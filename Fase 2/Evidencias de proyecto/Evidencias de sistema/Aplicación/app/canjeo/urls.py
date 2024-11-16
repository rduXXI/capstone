from django.urls import path
from . import views

urlpatterns = [
    path("canjear/", views.canjear_producto, name="canjear"),
    path('canje/<int:orden_id>/aprobar/', views.aprobar_rechazar_canje, {'accion': 'aprobar'}, name='aprobar_canje'),
    path('canje/<int:orden_id>/rechazar/', views.aprobar_rechazar_canje, {'accion': 'rechazar'}, name='rechazar_canje'),
]
