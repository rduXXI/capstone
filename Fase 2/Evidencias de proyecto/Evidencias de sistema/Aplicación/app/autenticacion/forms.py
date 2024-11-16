from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from roles.models import Empleado


class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    run = forms.CharField(max_length=10, required=True, label="RUN")
    dv = forms.CharField(max_length=1, required=True, label="Dígito Verificador")
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "group",
            "run",
            "dv",
            "direccion",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Empleado.objects.create(
                usuario=user,
                run=self.cleaned_data["run"],
                dv=self.cleaned_data["dv"],
                direccion=self.cleaned_data["direccion"],
            )
        return user
