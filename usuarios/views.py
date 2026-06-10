"""Vistas de usuarios: registro y perfil editable."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ProfileForm, RegistroForm
from .models import Profile


class RegistroView(CreateView):
    """Alta de usuario. Tras registrarse, redirige al login."""

    form_class = RegistroForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("usuarios:login")

    def form_valid(self, form):
        messages.success(self.request, "Cuenta creada. Ya podés iniciar sesión.")
        return super().form_valid(form)


class PerfilView(LoginRequiredMixin, UpdateView):
    """Edición del perfil propio (LoginRequiredMixin: requiere sesión)."""

    form_class = ProfileForm
    template_name = "usuarios/perfil.html"
    success_url = reverse_lazy("usuarios:perfil")

    def get_object(self, queryset=None):
        # Siempre el perfil del usuario logueado: nadie puede editar otro
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado.")
        return super().form_valid(form)
