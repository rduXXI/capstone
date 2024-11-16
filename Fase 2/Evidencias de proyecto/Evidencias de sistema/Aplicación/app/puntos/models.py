from django.db import models
from roles.models import Empleado


class TransaccionPuntos(models.Model):
    perfil = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    puntos = models.IntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.perfil.usuario.first_name} {self.perfil.usuario.last_name} hizo uso de  {self.puntos} puntos."
