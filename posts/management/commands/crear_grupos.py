"""Comando de gestión: crea el grupo Moderadores con su permiso custom.

Uso:
    python manage.py crear_grupos

Es idempotente: se puede ejecutar varias veces sin duplicar nada.
Se documenta en el README como paso de configuración inicial, y se
ejecuta también en el servidor al deployar.
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el grupo 'Moderadores' y le asigna el permiso puede_moderar."

    def handle(self, *args, **options):
        grupo, creado = Group.objects.get_or_create(name="Moderadores")
        permiso = Permission.objects.get(
            codename="puede_moderar",
            content_type__app_label="posts",
        )
        grupo.permissions.add(permiso)
        estado = "creado" if creado else "ya existía"
        self.stdout.write(
            self.style.SUCCESS(
                f"Grupo 'Moderadores' {estado}, permiso 'puede_moderar' asignado."
            )
        )
