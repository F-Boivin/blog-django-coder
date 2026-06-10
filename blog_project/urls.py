"""URLs raíz del proyecto blog.

Delega a las apps con include() y namespacing:
- /            → posts (listado, búsqueda, detalle, CRUD, About, Contacto)
- /usuarios/   → registro, login, logout, perfil
- /admin/      → panel de administración
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path("usuarios/", include("usuarios.urls")),
]
