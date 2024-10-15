from django.urls import path
from autenticacion.views import cerrar_sesion, register, listado_usuarios

urlpatterns = [
    path('logout/', cerrar_sesion, name='logout'),
    path('register/', register, name='register'),
    path('usuarios/', listado_usuarios, name='listado_usuarios'),
]