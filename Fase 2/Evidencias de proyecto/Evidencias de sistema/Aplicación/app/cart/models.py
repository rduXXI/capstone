from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto


class CartItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

    def get_total_points(self):
        return self.producto.puntos_requeridos * self.cantidad
