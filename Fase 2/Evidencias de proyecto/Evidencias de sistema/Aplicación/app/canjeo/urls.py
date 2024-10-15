from django.urls import path
from canjeo.views import canjear_producto, obtener_canjeos

urlpatterns = [
    path('canjear/<int:producto_id>/', canjear_producto, name='canjear'),
    path('obtener_canjeos/', obtener_canjeos, name='obtener_canjeos'),
]