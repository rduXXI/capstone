from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from productos.models import Producto
from roles.models import Empleado
from .models import CartItem

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = request.POST.get('cantidad', 1)  # Obtén la cantidad de la solicitud POST, o asigna 1 por defecto
    cantidad = int(cantidad)  # Convierte la cantidad a entero

    # Verifica que la cantidad sea válida (mayor que 0)
    if cantidad <= 0:
        cantidad = 1  # Si la cantidad es 0 o negativa, asigna 1

    # Busca si el producto ya está en el carrito
    cart_item, creado = CartItem.objects.get_or_create(usuario=request.user, producto=producto)
    
    if creado:
        cart_item.cantidad = cantidad  # Si el artículo es nuevo, asigna la cantidad
    else:
        cart_item.cantidad += cantidad  # Si el artículo ya está en el carrito, incrementa la cantidad
    
    cart_item.save()
    
    return redirect('ver_carrito')  # Redirige a la vista del carrito

def ver_carrito(request):
    cart_items = CartItem.objects.filter(usuario=request.user)
    total_precio = sum(item.get_total_price() for item in cart_items)
    total_puntos = sum(item.get_total_points() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_precio': total_precio,
        'total_puntos': total_puntos,
    }
    
    return render(request, 'carrito/ver_carrito.html', context)

def actualizar_cantidad_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, usuario=request.user)
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad > 0:
        cart_item.cantidad = cantidad
        cart_item.save()
    else:
        cart_item.delete()  # Elimina el item si la cantidad es 0 o menor

    return redirect('ver_carrito')


def eliminar_del_carrito(request, carrito_item_id):
    carrito_item = get_object_or_404(CartItem, id=carrito_item_id)
    carrito_item.delete()
    return redirect("ver_carrito")




