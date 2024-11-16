from django.contrib.auth.models import User
from django.db import models


class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Empleado", verbose_name="Usuario")
    run = models.CharField(max_length=10)
    dv = models.CharField(max_length=1)
    direccion = models.CharField(max_length=255)
    puntos = models.PositiveIntegerField(default=1000)
    puntos_subasta = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return self.usuario.username
