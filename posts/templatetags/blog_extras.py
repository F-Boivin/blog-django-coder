"""Tags y filtros personalizados del blog (M11-U4 y U8)."""

from django import template

register = template.Library()


@register.filter(name="resumen")
def resumen(value, longitud=120):
    """Filtro: recorta el texto a `longitud` caracteres con elipsis.

    Uso: {{ post.content|resumen:120 }}
    """
    texto = str(value)
    if len(texto) <= longitud:
        return texto
    return texto[:longitud].rstrip() + "…"


@register.inclusion_tag("posts/tarjeta_post.html")
def tarjeta_post(post, user):
    """Inclusion tag: renderiza la tarjeta de una publicación.

    Componente reutilizable (M11-U8): encapsula el HTML de la tarjeta
    y la lógica de qué botones mostrar según el usuario.

    Uso: {% tarjeta_post post user %}
    """
    puede_editar = user.is_authenticated and user == post.author
    puede_borrar = user.is_authenticated and (
        user == post.author or user.has_perm("posts.puede_moderar")
    )
    return {
        "post": post,
        "puede_editar": puede_editar,
        "puede_borrar": puede_borrar,
    }
