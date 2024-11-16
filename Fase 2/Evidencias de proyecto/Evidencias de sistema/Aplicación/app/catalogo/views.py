from django.shortcuts import render
from productos.models import Producto
from roles.models import Empleado



def view_catalogo(request):
    productos = Producto.objects.all().order_by("categoria__nombre", "nombre")
    empleado = Empleado.objects.get(usuario=request.user)
    context = {
        "productos": productos,
        "empleado": empleado,
    }
    return render(request, "components/roles/catalogo.html", context)

def lista_catalogo(request):
    productos = Producto.objects.all().order_by("categoria__nombre", "nombre")
    empleado = Empleado.objects.get(usuario=request.user)
    context = {
        "productos": productos,
        "empleado": empleado,
    }
    return render(request, "components/app_catalogo/catalogo_modo_lista.html", context)