from django import forms
from roles.models import Empleado


class AsignarPuntosForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = {
            "puntos",
            "puntos_subasta",
        }


class PuntosForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = {
            "usuario",
            "puntos",
            "puntos_subasta",
        }


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = {
            "run",
            "dv",
            "direccion",
        }
