from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from canjeo.models import Canjeo
from orden_pedido.models import OrdenPedido, ProductoCanjeado
from productos.models import Producto
from puntos.models import TransaccionPuntos
from roles.models import Empleado


def canjear_producto(request):
    perfil = Empleado.objects.get(usuario=request.user)

    # Obtener la lista de productos seleccionados
    productos_seleccionados = request.POST.getlist("productos")

    # Verificar si no se seleccionó ningún producto
    if not productos_seleccionados:
        messages.error(request, "No has seleccionado ningún producto para canjear.")
        return redirect("catalogo")

    total_puntos_requeridos = 0
    productos_a_canjear = []

    # Procesar los productos seleccionados
    for producto_id in productos_seleccionados:
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get(f"cantidad_{producto_id}", 1))
        total_puntos_requeridos += producto.puntos_requeridos * cantidad

        if producto.stock >= cantidad:
            productos_a_canjear.append((producto, cantidad))
        else:
            messages.error(
                request, f"El producto {producto.nombre} no tiene suficiente stock."
            )
            return redirect("catalogo")

    # Verificar si el usuario tiene suficientes puntos
    if perfil.puntos >= total_puntos_requeridos:
        orden_pedido = OrdenPedido.objects.create(
            empleado=perfil.usuario,
            razon_social=perfil,
            total_puntos=total_puntos_requeridos,
            estado="Pendiente",
        )

        for producto, cantidad in productos_a_canjear:
            puntos_gastados = producto.puntos_requeridos * cantidad

            perfil.puntos -= puntos_gastados
            perfil.save()

            # Registrar la transacción de puntos
            TransaccionPuntos.objects.create(perfil=perfil, puntos=-puntos_gastados)

            # Registrar el canje
            Canjeo.objects.create(
                perfil=perfil.usuario,
                producto=producto,
                puntos_gastados=puntos_gastados,
                cantidad=cantidad,
            )

            # Agregar los productos canjeados a la orden
            ProductoCanjeado.objects.create(
                orden=orden_pedido,
                producto=producto,
                cantidad=cantidad,
                puntos_gastados=puntos_gastados,
            )

            # Actualizar el stock del producto
            producto.stock -= cantidad
            producto.save()

        messages.success(
            request, "Productos canjeados con éxito y orden de pedido creada."
        )
        return redirect("catalogo")
    else:
        messages.error(
            request,
            "No tienes suficientes puntos para canjear los productos seleccionados.",
        )
        return redirect("catalogo")


def aprobar_rechazar_canje(request, orden_id, accion):
    # Obtener la orden de pedido
    orden_pedido = get_object_or_404(OrdenPedido, id=orden_id)

    # Verificar si la orden ya ha sido procesada (aprobada o rechazada)
    if orden_pedido.estado != "Pendiente":
        messages.error(request, "Esta orden ya ha sido procesada.")
        return redirect("ordenes")  # Vista de administración de canjeos

    # Procesar la acción de acuerdo al parámetro 'accion'
    if accion == "aprobar":
        # Aprobar la orden
        orden_pedido.estado = "Aprobada"
        orden_pedido.save()

        messages.success(request, "La orden ha sido aprobada exitosamente.")
        return redirect("ordenes")

    elif accion == "rechazar":
        # Rechazar la orden y reembolsar los puntos al empleado
        perfil = Empleado.objects.get(usuario=orden_pedido.empleado)

        # Reembolsar los puntos y restablecer el stock de los productos
        productos_canjeados = ProductoCanjeado.objects.filter(orden=orden_pedido)
        for producto_canjeado in productos_canjeados:
            producto = producto_canjeado.producto
            cantidad = producto_canjeado.cantidad
            puntos_reembolsados = producto_canjeado.puntos_gastados

            # Reembolsar puntos al empleado
            perfil.puntos += puntos_reembolsados
            perfil.save()

            # Restablecer el stock del producto
            producto.stock += cantidad
            producto.save()

            # Registrar la transacción de reembolso
            TransaccionPuntos.objects.create(perfil=perfil, puntos=puntos_reembolsados)

        # Cambiar el estado de la orden a 'rechazada'
        orden_pedido.estado = "Rechazada"
        orden_pedido.save()

        messages.success(
            request, "La orden ha sido rechazada y los puntos han sido reembolsados."
        )
        return redirect("ordenes")

    else:
        messages.error(request, "Acción no válida.")
        return redirect("ordenes")
