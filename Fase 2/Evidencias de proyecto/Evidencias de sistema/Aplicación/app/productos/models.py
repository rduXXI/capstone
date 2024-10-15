from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(verbose_name='Categoría', max_length=255)
    
    def __str__(self):
        return self.nombre
    
class Marca(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    
    def __str__(self):
        return self.nombre
    
class PaisOrigen(models.Model):
    codigo_iso = models.CharField(verbose_name='Código ISO', max_length=255)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    
    def __str__(self):
        return self.codigo_iso
    
class Proveedor(models.Model):
    rut = models.CharField(verbose_name='RUT', max_length=255)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    telefono = models.CharField(verbose_name='Teléfono', max_length=255)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    abv = models.FloatField(verbose_name='Alc. (%)')
    contenido = models.FloatField(verbose_name='Cont. Neto (ml)')
    envase = models.CharField(verbose_name='Envase', max_length=255)
    puntos_requeridos = models.PositiveIntegerField(verbose_name='Puntos Requeridos')
    precio = models.FloatField(verbose_name='Precio (CLP)')
    stock = models.PositiveIntegerField(verbose_name='Stock', default=0)
    unidades = models.PositiveIntegerField(verbose_name='Unidades', default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name='Marca')
    pais_origen = models.ForeignKey(PaisOrigen, on_delete=models.CASCADE, verbose_name='País de Origen')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    
    def __str__(self):
        return self.nombre