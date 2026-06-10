"""Formularios del blog: PostForm (ModelForm), BusquedaForm y ContactForm.

Cada formulario demuestra un tipo distinto:
- PostForm: ModelForm clásico para crear/editar publicaciones.
- BusquedaForm: Form de filtrado vía GET (búsqueda dinámica).
- ContactForm: Form manual con validación personalizada en clean_*.
"""

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categoria"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 8}),
        }

    def clean_title(self):
        """El título debe tener al menos 5 caracteres."""
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError(
                "El título debe tener al menos 5 caracteres."
            )
        return title


class BusquedaForm(forms.Form):
    """Formulario de búsqueda (se envía por GET, no modifica datos)."""

    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Título o contenido…"}),
    )
    categoria = forms.ChoiceField(
        label="Categoría",
        required=False,
        choices=[("", "Todas")] + Post.CATEGORIA_CHOICES,
    )


class ContactForm(forms.Form):
    """Formulario de contacto con validación personalizada."""

    nombre = forms.CharField(label="Nombre", max_length=100)
    email = forms.EmailField(label="Email")
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    def clean_mensaje(self):
        """El mensaje debe tener al menos 10 caracteres útiles."""
        mensaje = self.cleaned_data["mensaje"].strip()
        if len(mensaje) < 10:
            raise forms.ValidationError(
                "El mensaje debe tener al menos 10 caracteres."
            )
        return mensaje
