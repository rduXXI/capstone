from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
from roles.models import Empleado

class OrdenPedido(models.Model):
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordenes_pedido")
    razon_social = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="razon_social")
    estado = models.CharField(max_length=20, default='Pendiente')  # 'pendiente', 'aprobada', 'rechazada'
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total_puntos = models.IntegerField()

    def __str__(self):
        return f"Orden de Pedido #{self.id} - {self.empleado.username}"

class ProductoCanjeado(models.Model):
    orden = models.ForeignKey(OrdenPedido, on_delete=models.CASCADE, related_name="productos_canjeados")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    puntos_gastados = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - Cantidad: {self.cantidad}"
