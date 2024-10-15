from django.contrib import admin
from productos.models import Categoria, Marca, PaisOrigen, Producto, Proveedor

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(PaisOrigen)
admin.site.register(Producto)
admin.site.register(Proveedor)