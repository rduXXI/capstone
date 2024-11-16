from django.urls import path
from . import views

urlpatterns = [
    path("categoria/", views.categoria, name="categorias"),
    path("marca/", views.marca, name="marcas"),
    path("procedencia/", views.procedencia, name="procedencias"),
    path("producto/", views.producto, name="productos"),
    path("proveedor/", views.proveedor, name="proveedores"),
    path("categoria/add/", views.add_categoria, name="add_categoria"),
    path("marca/add/", views.add_marca, name="add_marca"),
    path("procedencia/add/", views.add_procedencia, name="add_procedencia"),
    path("producto/add/", views.add_producto, name="add_producto"),
    path("proveedor/add/", views.add_proveedor, name="add_proveedor"),
]
