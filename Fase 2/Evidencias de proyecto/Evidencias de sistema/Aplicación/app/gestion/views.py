from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from gestion.forms import MovimientoInventarioForm, ProductoForm

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('obtener_productos')
        
    else:
        form = ProductoForm()
        
    return render(request, 'components/crear_producto.html', {'form': form})

@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.supervisor = request.user
            movimiento.save()
            producto = movimiento.producto
            
            if movimiento.tipo == 'entrada':
                producto.stock += movimiento.stock
                
            elif movimiento.tipo == 'salida' and producto.stock >= movimiento.stock:
                producto.stock -= movimiento.stock
            producto.save()
            
            return redirect('obtener_productos')

    else:
        form = MovimientoInventarioForm()
        
    return render(request, 'components/registrar_movimiento.html', {'form': form})
