from django.contrib.auth.models import Group, Permission
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from canjeo.models import Canjeo
from orden_pedido.models import OrdenPedido
from productos.models import Producto
from roles.models import Empleado
from sorteo.models import Sorteo
from subasta.models import Subasta

admin.site.register(Empleado)

def create_groups():
    # Crear o obtener el grupo 'Empleados'
    empleados_group, empleados_created = Group.objects.get_or_create(name="Empleados")
    print("Grupo Empleados:", "Creado" if empleados_created else "Ya existía")

    # Crear o obtener el grupo 'Supervisores'
    supervisores_group, supervisores_created = Group.objects.get_or_create(name="Supervisores")
    print("Grupo Supervisores:", "Creado" if supervisores_created else "Ya existía")

    # Obtener tipos de contenido para los permisos
    canjeo_content_type = ContentType.objects.get_for_model(Canjeo)
    sorteo_content_type = ContentType.objects.get_for_model(Sorteo)
    subasta_content_type = ContentType.objects.get_for_model(Subasta)
    orden_pedido_content_type = ContentType.objects.get_for_model(OrdenPedido)
    producto_content_type = ContentType.objects.get_for_model(Producto)

    # Obtener permisos por tipo de contenido
    canjeo_permissions = Permission.objects.filter(content_type=canjeo_content_type)
    sorteo_permissions = Permission.objects.filter(content_type=sorteo_content_type)
    subasta_permissions = Permission.objects.filter(content_type=subasta_content_type)
    orden_pedido_permissions = Permission.objects.filter(content_type=orden_pedido_content_type)
    producto_permissions = Permission.objects.filter(content_type=producto_content_type)

    # Asignar permisos al grupo 'Empleados'
    empleados_all_permissions = canjeo_permissions | sorteo_permissions | subasta_permissions
    empleados_group.permissions.set(empleados_all_permissions)
    print("Permisos asignados a Empleados:", empleados_all_permissions)

    # Asignar permisos al grupo 'Supervisores'
    supervisores_all_permissions = orden_pedido_permissions | producto_permissions
    supervisores_group.permissions.set(supervisores_all_permissions)
    print("Permisos asignados a Supervisores:", supervisores_all_permissions)

# Llama a la función en un lugar seguro, como un management command o señal `post_migrate`
