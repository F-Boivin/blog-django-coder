"""Admin personalizado para Post.

Aplica las técnicas del Módulo 11: list_display, list_filter,
search_fields, list_select_related (performance), date_hierarchy y una
acción personalizada de moderación.
"""

from django.contrib import admin

from .models import Post


@admin.action(description="Marcar categoría como 'Noticias'")
def marcar_como_noticias(modeladmin, request, queryset):
    actualizados = queryset.update(categoria="noticias")
    modeladmin.message_user(
        request, f"{actualizados} publicaciones movidas a Noticias."
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "categoria", "created_at")
    list_filter = ("categoria", "created_at", "author")
    search_fields = ("title", "content", "author__username")
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    # Performance: resuelve la FK author con un JOIN (evita N+1 en el listado)
    list_select_related = ("author",)
    actions = [marcar_como_noticias]
