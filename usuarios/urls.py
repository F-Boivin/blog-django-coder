"""URLs de usuarios: login/logout built-in + registro y perfil propios."""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import PerfilView, RegistroView


app_name = "usuarios"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="usuarios/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("perfil/", PerfilView.as_view(), name="perfil"),
]
