from django import forms
from gestion.models import MovimientoInventario
from productos.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'abv',
            'contenido',
            'envase',
            'puntos_requeridos',
            'precio',
            'stock',
            'unidades',
            'categoria',
            'marca',
            'pais_origen',
            'proveedor',
        ]

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'tipo', 'stock']