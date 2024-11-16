from django.urls import path
from . import views

urlpatterns = [
    path("logout/", views.cerrar_sesion, name="logout"),
    path("register/", views.register, name="register"),
    path("usuarios/", views.listado_usuarios, name="usuarios"),
]
