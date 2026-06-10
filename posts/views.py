"""Vistas del blog.

Arquitectura de permisos (3 niveles):
- Público: listado con búsqueda, detalle, About, Contacto.
- Usuario registrado: crear posts y editar los propios
  (LoginRequiredMixin + UserPassesTestMixin).
- Moderadores: eliminar cualquier publicación, vía el permiso
  personalizado posts.puede_moderar (el autor también puede borrar la suya).
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import BusquedaForm, ContactForm, PostForm
from .models import Post


class PostListView(ListView):
    """Listado público con búsqueda dinámica vía GET.

    La búsqueda usa icontains (insensible a mayúsculas) sobre título y
    contenido con Q objects (OR), y encadena un segundo filtro por
    categoría si se seleccionó una. select_related evita N+1 al mostrar
    el autor de cada post.
    """

    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.select_related("author")
        q = self.request.GET.get("q", "").strip()
        categoria = self.request.GET.get("categoria", "").strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )
        if categoria:
            # Filtro encadenado: se combina con la búsqueda anterior
            queryset = queryset.filter(categoria=categoria)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["busqueda_form"] = BusquedaForm(self.request.GET or None)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.select_related("author")


class PostCreateView(LoginRequiredMixin, CreateView):
    """Crear publicación: requiere usuario autenticado."""

    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("posts:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Publicación creada correctamente.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar publicación: solo el autor."""

    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("posts:post-list")

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar publicación: el autor o un usuario con permiso de moderación.

    Acá se aplica el permiso personalizado posts.puede_moderar (asignado
    al grupo Moderadores): un moderador puede eliminar publicaciones de
    cualquier autor, requisito de control de acceso por permisos.
    """

    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("posts:post-list")
    context_object_name = "post"

    def test_func(self):
        user = self.request.user
        return (
            user == self.get_object().author
            or user.has_perm("posts.puede_moderar")
        )


class AboutView(TemplateView):
    """Página estática 'Acerca de'."""

    template_name = "posts/about.html"


class ContactoView(FormView):
    """Página de contacto con formulario validado."""

    template_name = "posts/contacto.html"
    form_class = ContactForm
    success_url = reverse_lazy("posts:contacto")

    def form_valid(self, form):
        # En un proyecto real acá se enviaría un email (send_mail).
        # Para este alcance, se confirma la recepción al usuario.
        messages.success(
            self.request,
            f"¡Gracias {form.cleaned_data['nombre']}! Tu mensaje fue recibido.",
        )
        return super().form_valid(form)
