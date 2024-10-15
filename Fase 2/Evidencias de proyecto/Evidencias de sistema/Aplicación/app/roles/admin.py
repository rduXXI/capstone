from django.contrib import admin
from roles.models import Empleado, Rol

admin.site.register(Rol)
admin.site.register(Empleado)