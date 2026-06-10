#!/usr/bin/env python
"""Utility de Django para tareas administrativas del proyecto blog."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y el entorno virtual "
            "activado? Verificá con 'pip install -r requirements.txt'."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
