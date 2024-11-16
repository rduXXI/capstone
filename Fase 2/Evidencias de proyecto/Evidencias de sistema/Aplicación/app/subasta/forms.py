from django import forms
from productos.models import Producto
from subasta.models import Subasta


class SubastaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "required": "required"}),
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Selecciona una fecha",
                "type": "date",
                "required": "required",
            }
        )
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Selecciona una fecha",
                "type": "date",
                "required": "required",
            }
        )
    )

    class Meta:
        model = Subasta
        fields = [
            "producto",
            "fecha_inicio",
            "fecha_fin",
        ]
