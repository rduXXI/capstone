from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Rol(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Rol', verbose_name='Usuario')
    
    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        ordering = ['-id']
        

class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Empleado', verbose_name='Usuario')
    puntos = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.usuario.username