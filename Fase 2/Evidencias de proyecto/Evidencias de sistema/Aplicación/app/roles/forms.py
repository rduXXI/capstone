from django import forms
from django.contrib.auth.models import User
from roles.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = {
            'puntos',
        }
        
class PuntosForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = {
            'usuario',
            'puntos',
        }