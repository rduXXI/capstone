from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto

# Create your models here.

class MovimientoInventario(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    stock = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tipo.capitalize()} de {self.stock} {self.producto.nombre}'