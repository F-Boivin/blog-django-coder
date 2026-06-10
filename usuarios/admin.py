"""Admin de usuarios: Profile como INLINE dentro del User (M11-U12).

Al editar un usuario en el admin, su perfil aparece embebido en la
misma página — el patrón de inlines para relaciones uno-a-uno.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "perfil"


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ("username", "email", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_superuser", "groups")


# Re-registrar User con el admin extendido (incluye el inline de Profile)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
