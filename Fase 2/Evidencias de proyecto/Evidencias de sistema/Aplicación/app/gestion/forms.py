from django import forms
from gestion.models import MovimientoInventario
from productos.models import Producto


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["producto", "tipo", "stock"]
