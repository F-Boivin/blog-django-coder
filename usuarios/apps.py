from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"
    verbose_name = "Usuarios y perfiles"

    def ready(self):
        # Conecta la señal que crea el Profile automáticamente
        from . import signals  # noqa: F401
