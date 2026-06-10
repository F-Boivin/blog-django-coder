"""Context processor global del sitio (M11-U9).

Inyecta en TODOS los templates el nombre del sitio y el menú de
navegación, sin que cada vista tenga que pasarlos manualmente.
Registrado en settings.TEMPLATES OPTIONS context_processors.
"""


def datos_sitio(request):
    return {
        "site_name": "Blog Coder",
        "menu_items": [
            {"nombre": "Inicio", "url_name": "posts:post-list"},
            {"nombre": "Acerca de", "url_name": "posts:about"},
            {"nombre": "Contacto", "url_name": "posts:contacto"},
        ],
    }
