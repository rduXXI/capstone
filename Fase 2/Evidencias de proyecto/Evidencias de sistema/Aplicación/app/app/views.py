from django.shortcuts import redirect, render
from productos.models import Marca, Producto

def home(request):
    productos = Producto.objects.filter(destacado=True).all
    marcas = Marca.objects.all().order_by("nombre")
    context = {
            "marcas": marcas,
            "productos": productos,
        }
    
    if request.user.is_staff:
        return redirect("productos")
    elif request.user.groups.filter(name="Supervisores").exists():
        return redirect("productos")
    else:
        
        return render(request, "home/home.html", context)
