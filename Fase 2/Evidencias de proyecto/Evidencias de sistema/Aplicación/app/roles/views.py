from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from . import forms
from roles.models import Empleado
from django.contrib import messages


@login_required
def add_puntos(request):
    if request.method == "POST":
        form = forms.PuntosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios")
    else:
        form = forms.PuntosForm()
    return render(request, "components/roles/add_puntos.html", {"form": form})


@login_required
def change_puntos(request, id=None):
    if id:
        empleado = get_object_or_404(Empleado, id=id)
    else:
        empleado = None
    if request.method == "POST":
        form = forms.AsignarPuntosForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Guardado correctamente")
            context = {"form": form}
            return redirect("usuarios")
        else:
            context = {"form": form}
    else:
        form = forms.AsignarPuntosForm(instance=empleado)
        context = {"form": form}
    return render(request, "components/roles/change_puntos.html", context)