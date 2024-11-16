from django import forms
from . import models


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = models.Categoria
        fields = ["nombre"]


class MarcaForm(forms.ModelForm):
    class Meta:
        model = models.Marca
        fields = [
            "nombre",
            "imagen",
        ]


class ProcedenciaForm(forms.ModelForm):
    class Meta:
        model = models.Procedencia
        fields = ["codigo_iso", "nombre"]


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = models.Proveedor
        fields = ["rut", "nombre", "telefono"]


class ProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = [
            "nombre",
            "descripcion",
            "abv",
            "contenido",
            "puntos_requeridos",
            "categoria",
            "marca",
            "pais_origen",
            "proveedor",
            "imagen",
        ]
