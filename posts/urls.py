"""URLs de la app posts, con namespacing."""

from django.urls import path

from . import views


app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("posts/nuevo/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="post-delete"),
    path("acerca-de/", views.AboutView.as_view(), name="about"),
    path("contacto/", views.ContactoView.as_view(), name="contacto"),
]
