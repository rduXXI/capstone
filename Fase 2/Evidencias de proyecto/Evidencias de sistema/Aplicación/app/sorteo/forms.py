from django import forms
from .models import Sorteo


class ParticiparSorteoForm(forms.ModelForm):
    class Meta:
        model = Sorteo
        fields = [
            "producto",
        ]
