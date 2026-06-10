"""Tests de formularios y vistas principales (requisito U15-6).

Cubren: validación de PostForm y ContactForm, listado público, búsqueda
dinámica con filtros encadenados, control de acceso por login y el
permiso personalizado de moderación.
"""

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm, PostForm
from .models import Post


class FormTests(TestCase):
    def test_postform_titulo_corto_invalido(self):
        form = PostForm(data={"title": "abc", "content": "x", "categoria": "opinion"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_postform_valido(self):
        form = PostForm(
            data={"title": "Título válido", "content": "Contenido", "categoria": "opinion"}
        )
        self.assertTrue(form.is_valid())

    def test_contactform_mensaje_corto_invalido(self):
        form = ContactForm(
            data={"nombre": "Ana", "email": "ana@example.com", "mensaje": "corto"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("mensaje", form.errors)

    def test_contactform_email_invalido(self):
        form = ContactForm(
            data={"nombre": "Ana", "email": "no-es-email", "mensaje": "Mensaje suficientemente largo"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class VistasTests(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(username="autor", password="clave1234!")
        self.otro = User.objects.create_user(username="otro", password="clave1234!")
        self.post = Post.objects.create(
            title="Post de prueba",
            content="Contenido sobre Django",
            categoria="tutorial",
            author=self.autor,
        )

    def test_listado_publico(self):
        response = self.client.get(reverse("posts:post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post de prueba")

    def test_busqueda_icontains(self):
        Post.objects.create(
            title="Otra cosa", content="Sin relación", categoria="opinion", author=self.autor
        )
        response = self.client.get(reverse("posts:post-list"), {"q": "django"})
        self.assertContains(response, "Post de prueba")
        self.assertNotContains(response, "Otra cosa")

    def test_busqueda_filtros_encadenados(self):
        response = self.client.get(
            reverse("posts:post-list"), {"q": "django", "categoria": "opinion"}
        )
        # Coincide el texto pero no la categoría → no aparece
        self.assertNotContains(response, "Post de prueba")

    def test_crear_requiere_login(self):
        response = self.client.get(reverse("posts:post-create"))
        self.assertEqual(response.status_code, 302)

    def test_editar_solo_autor(self):
        self.client.login(username="otro", password="clave1234!")
        response = self.client.get(
            reverse("posts:post-update", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_moderador_puede_borrar_post_ajeno(self):
        call_command("crear_grupos")
        moderador = User.objects.create_user(username="mod", password="clave1234!")
        moderador.groups.add(Group.objects.get(name="Moderadores"))
        self.client.login(username="mod", password="clave1234!")
        response = self.client.get(
            reverse("posts:post-delete", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
