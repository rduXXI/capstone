from django import forms
from django.contrib.auth.models import User
from .models import Categoria, Marca, PaisOrigen, Producto, Proveedor

class CategoriaForm(forms.ModelForm):
    
    class Meta:
        model = Categoria
        fields = ['nombre']
        
class MarcaForm(forms.ModelForm):
    
    class Meta:
        model = Marca
        fields = ['nombre']
        
class PaisOrigenForm(forms.ModelForm):
    
    class Meta:
        model = PaisOrigen
        fields = ['codigo_iso', 'nombre']
        
class ProveedorForm(forms.ModelForm):
    
    class Meta:
        model = Proveedor
        fields = ['rut', 'nombre', 'telefono']
        
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
            'abv',
            'puntos_requeridos',
            'proveedor',
        ]