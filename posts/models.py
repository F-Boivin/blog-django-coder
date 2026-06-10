"""Modelo Post del blog.

Incluye un permiso personalizado (puede_moderar) que se asigna al grupo
"Moderadores" (ver el comando de gestión crear_grupos). Las vistas usan
ese permiso para autorizar la moderación de publicaciones ajenas.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Post(models.Model):
    """Publicación del blog, escrita por un usuario registrado."""

    CATEGORIA_CHOICES = [
        ("tecnologia", "Tecnología"),
        ("opinion", "Opinión"),
        ("tutorial", "Tutorial"),
        ("noticias", "Noticias"),
    ]

    title = models.CharField("título", max_length=200)
    content = models.TextField("contenido")
    categoria = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default="tecnologia"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="autor",
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"
        permissions = [
            ("puede_moderar", "Puede moderar publicaciones de cualquier autor"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})
