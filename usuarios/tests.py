"""Tests de la app usuarios: registro, señal de Profile y acceso al perfil."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsuariosTests(TestCase):
    def test_signal_crea_profile(self):
        user = User.objects.create_user(username="nuevo", password="clave1234!")
        self.assertTrue(hasattr(user, "profile"))

    def test_registro_crea_usuario(self):
        response = self.client.post(
            reverse("usuarios:registro"),
            {
                "username": "felipe_test",
                "email": "felipe@example.com",
                "password1": "UnaClaveSegura99",
                "password2": "UnaClaveSegura99",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="felipe_test").exists())

    def test_perfil_requiere_login(self):
        response = self.client.get(reverse("usuarios:perfil"))
        self.assertEqual(response.status_code, 302)

    def test_perfil_con_login(self):
        User.objects.create_user(username="logueado", password="clave1234!")
        self.client.login(username="logueado", password="clave1234!")
        response = self.client.get(reverse("usuarios:perfil"))
        self.assertEqual(response.status_code, 200)
