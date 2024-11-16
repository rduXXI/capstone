from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . import forms


@login_required
def add_movimiento(request):
    if request.method == "POST":
        form = forms.MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.supervisor = request.user
            movimiento.save()
            producto = movimiento.producto
            if movimiento.tipo == "entrada":
                producto.stock += movimiento.stock
            elif movimiento.tipo == "salida" and producto.stock >= movimiento.stock:
                producto.stock -= movimiento.stock
            producto.save()
            return redirect("productos")
    else:
        form = forms.MovimientoInventarioForm()
    context = {"form": form}
    return render(request, "components/gestion/add_movimiento.html", context)
