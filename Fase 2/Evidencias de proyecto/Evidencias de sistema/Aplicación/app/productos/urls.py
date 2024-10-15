from django.urls import path
from productos.views import add_marca, catalogo, obtener_productos, listado_categorias, crear_pais_origen, listado_proveedores, listado_marcas

urlpatterns = [
    path('obtener_productos/', obtener_productos, name='obtener_productos'),
    path('catalogo/', catalogo, name='catalogo'),
    path('listado_categorias/', listado_categorias, name='listado_categorias'),
    path('crear_pais_origen/', crear_pais_origen, name='crear_pais_origen'),
    path('proveedor/add', listado_proveedores, name='listado_proveedores'),
    path('marca/', listado_marcas, name='listado_marcas'),
    path('marca/add/', add_marca, name='add_marca'),
]