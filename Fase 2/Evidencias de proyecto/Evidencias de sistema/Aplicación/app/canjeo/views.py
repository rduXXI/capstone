from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from canjeo.models import Canjeo
from productos.models import Producto
from puntos.models import TransaccionPuntos
from roles.models import Empleado

@login_required
def canjear_producto(request, producto_id):
    
    producto = get_object_or_404(Producto, id=producto_id)
    perfil = Empleado.objects.get(usuario=request.user)
    
    if perfil.puntos >= producto.puntos_requeridos and producto.stock > 0:
        perfil.puntos -= producto.puntos_requeridos
        perfil.save()

        TransaccionPuntos.objects.create(
            perfil=perfil,
            puntos=-producto.puntos_requeridos
        )

        Canjeo.objects.create(
            perfil=perfil.usuario,
            producto=producto,
            puntos_gastados=producto.puntos_requeridos
        )

        producto.stock -= 1
        producto.save()
        
        return redirect('catalogo')
    else:
        return redirect('catalogo')

@login_required
def obtener_canjeos(request):
    canjeos = Canjeo.objects.all()
    
    return render(request, 'components/obtener_canjeos.html', {'canjeos': canjeos})