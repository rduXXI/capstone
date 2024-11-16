from django.urls import path
from . import views

urlpatterns = [
    path("crear_sorteo/", views.crear_sorteo, name="crear_sorteo"),
    path("cerrar_sorteo/<int:producto_id>/", views.cerrar_sorteo, name="cerrar_sorteo"),
    path("sorteo_admin/", views.sorteo_admin, name="sorteo_admin"),
    path("sorteo/", views.leer_sorteo, name="sorteos"),
    path("participar/<int:producto_id>/", views.participar_sorteo, name="participar"),
]
