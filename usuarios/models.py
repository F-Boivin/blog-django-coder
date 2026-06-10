"""Perfil de usuario, vinculado uno-a-uno con el User de Django.

El Profile se crea automáticamente al registrarse un usuario (ver
signals.py) y es editable desde la vista 'Mi perfil'.
"""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="usuario",
    )
    bio = models.TextField("biografía", blank=True)
    ubicacion = models.CharField("ubicación", max_length=100, blank=True)
    fecha_nacimiento = models.DateField("fecha de nacimiento", null=True, blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.user.username}"
