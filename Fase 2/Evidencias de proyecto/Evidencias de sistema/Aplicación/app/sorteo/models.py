from django.db import models
from productos.models import Producto
from roles.models import Empleado


class Sorteo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_sorteo = models.DateTimeField(auto_now_add=True)
    resultado = models.BooleanField(default=False)
    cerrado = models.BooleanField(default=False)

    def __str__(self):
        return f"Se ha publicado el sorteo de un {self.producto.descripcion} de {self.producto.nombre}"


class Participacion(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_participacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado.usuario.username} ha participado en el sorteo de un {self.sorteo.producto.descripcion} de {self.sorteo.producto.nombre} - Participación el {self.fecha_participacion}"
