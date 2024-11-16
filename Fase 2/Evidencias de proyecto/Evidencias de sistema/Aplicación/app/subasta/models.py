from django.db import models
from orden_pedido.models import OrdenPedido, ProductoCanjeado
from productos.models import Producto
from roles.models import Empleado


class Subasta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="subastas")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ganador = models.ForeignKey(Empleado, null=True, blank=True, on_delete=models.SET_NULL, related_name="subastas_ganadas")
    estado = models.CharField(max_length=20, default="Activa")

    def __str__(self):
        return f"Subasta de {self.producto.nombre} - Estado: {self.estado}"

    def cerrar_subasta(self):
        pujas = self.pujas.order_by("-puntos_ofrecidos")
        if pujas.exists():
            puja_ganadora = pujas.first()
            self.ganador = puja_ganadora.empleado
            self.estado = "Cerrada"

            # Reducir el stock del producto
            if self.producto.stock >= 1:
                self.producto.stock -= 1
                self.producto.save()

                # Crear una OrdenPedido para el ganador
                orden = OrdenPedido.objects.create(
                    empleado=self.ganador.usuario,
                    total_puntos=puja_ganadora.puntos_ofrecidos,
                )
                ProductoCanjeado.objects.create(
                    orden=orden,
                    producto=self.producto,
                    cantidad=1,
                    puntos_gastados=puja_ganadora.puntos_ofrecidos,
                )

            # Reembolsar puntos a los perdedores
            for puja in pujas[1:]:
                puja.empleado.puntos_subasta += puja.puntos_ofrecidos
                puja.empleado.save()

            self.save()
        else:
            self.estado = "Cerrada"
            self.save()


# Nueva clase Pujas para que los empleados puedan ofertar en las subastas
class Puja(models.Model):
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="pujas")
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="pujas")
    puntos_ofrecidos = models.PositiveIntegerField()

    def __str__(self):
        return f"Puja de {self.empleado.usuario.username} en {self.subasta.producto.nombre} por {self.puntos_ofrecidos} puntos"

    def save(self, *args, **kwargs):
        # Verificar que el empleado tenga suficientes puntos de subasta
        if self.empleado.puntos_subasta >= self.puntos_ofrecidos:
            # Reducir los puntos de subasta del empleado al pujar
            self.empleado.puntos_subasta -= self.puntos_ofrecidos
            self.empleado.save()
            super(Puja, self).save(*args, **kwargs)
        else:
            raise ValueError(
                "No tienes suficientes puntos de subasta para realizar esta puja"
            )