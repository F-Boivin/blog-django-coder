"""Formularios de registro y edición de perfil."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegistroForm(UserCreationForm):
    """Registro con email obligatorio."""

    email = forms.EmailField(
        required=True, help_text="Necesario para recuperar la cuenta."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    """Edición del perfil propio."""

    class Meta:
        model = Profile
        fields = ("bio", "ubicacion", "fecha_nacimiento")
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
