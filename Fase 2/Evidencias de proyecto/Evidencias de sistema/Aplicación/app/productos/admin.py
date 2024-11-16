from django.contrib import admin
from . import models

admin.site.register(models.Categoria)
admin.site.register(models.Marca)
admin.site.register(models.Procedencia)
admin.site.register(models.Producto)
admin.site.register(models.Proveedor)