from django.urls import path
from . import views

urlpatterns = [
    path("subastas/", views.subasta, name="lista_subastas"),
    path("subasta/<int:subasta_id>/pujar/", views.pujar, name="pujar"),
    path("historial_pujas/", views.historial_pujas, name="historial_pujas"),
    path("admin/subastas/", views.lista_subastas_admin, name="lista_subastas_admin"),
    path('admin/subasta/crear/', views.crear_subasta, name='crear_subasta'),
    path("admin/subasta/<int:subasta_id>/cerrar/", views.cerrar_subasta, name="cerrar_subasta"),
]
