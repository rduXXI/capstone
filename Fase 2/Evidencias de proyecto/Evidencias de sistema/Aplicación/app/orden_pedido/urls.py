from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.lista_ordenes_pedido, name='ordenes'),
    path('orden_pedido/<int:orden_id>/', views.detalle_orden_pedido, name='detalle_orden_pedido'),
    path('factura/<int:orden_id>/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('facturas/', views.lista_facturas, name='facturas'),
    path('factura/enviar/<int:orden_id>/', views.enviar_factura_email, name='enviar_factura_email'),
]