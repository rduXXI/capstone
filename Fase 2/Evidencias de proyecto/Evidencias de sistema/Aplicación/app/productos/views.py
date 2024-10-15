from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from productos.models import Producto, Categoria, Marca, PaisOrigen, Proveedor
from productos.forms import CategoriaForm, MarcaForm, PaisOrigenForm, ProductoForm, ProveedorForm
from roles.models import Empleado

@login_required
def obtener_productos(request):
    productos = Producto.objects.all()
    
    return render(request, 'components/obtener_productos.html', {'productos': productos})

def catalogo(request):
    empleado = Empleado.objects.get(usuario=request.user)
    productos = Producto.objects.all()
    context = {
        'productos': productos,
        'empleado': empleado,
    }
    
    return render(request, 'components/catalogo.html', context)

@login_required
def listado_categorias(request):
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('listado_categorias')
        
    else:
        form = CategoriaForm()
        
    context = {
        'form': form,
        'categorias': categorias,
    }
    
    return render(request, 'components/listado_categorias.html', context)

@login_required
def listado_marcas(request):
    marcas = Marca.objects.all()
    
    return render(request, 'components/listado_marcas.html', {'marcas': marcas})

@login_required
def add_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('obtener_productos')
    else:
        form = MarcaForm()
    return render(request, 'components/crear_marca.html', {'form': form})

@login_required
def crear_pais_origen(request):
    if request.method == 'POST':
        form = PaisOrigenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('obtener_productos')
    else:
        form = PaisOrigenForm()
    return render(request, 'components/crear_pais_origen.html', {'form': form})

@login_required
def listado_proveedores(request):
    proveedores = Proveedor.objects.all()
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_proveedores')
    else:
        form = ProveedorForm()
    
    context = {
        'form': form,
        'proveedores': proveedores
    }
    
    return render(request, 'components/listado_proveedores.html', context)

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