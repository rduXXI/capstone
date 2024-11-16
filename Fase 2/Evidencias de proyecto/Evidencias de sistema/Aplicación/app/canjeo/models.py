from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto


class Canjeo(models.Model):
    perfil = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    puntos_gastados = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.perfil.username} canjeó {self.cantidad} unidades de {self.producto.nombre} a las {self.created_at}"
