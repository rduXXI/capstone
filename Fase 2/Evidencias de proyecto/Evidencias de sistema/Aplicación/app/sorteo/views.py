from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from orden_pedido.models import OrdenPedido, ProductoCanjeado
from .models import Participacion, Producto, Sorteo, Empleado
import random


@login_required
@staff_member_required
def sorteo_admin(request):
    sorteo_activo = Sorteo.objects.filter(cerrado=False).first()

    if sorteo_activo:
        # Filtra las participaciones que pertenecen al sorteo activo
        participaciones = Participacion.objects.filter(sorteo=sorteo_activo)
        producto = sorteo_activo.producto
        context = {
            "participaciones": participaciones,
            "producto": producto,
            "sorteo": sorteo_activo,
        }
    else:
        context = {
            "sorteo": None,
        }

    return render(request, "components/app_sorteo/sorteo_admin.html", context)


@login_required
@staff_member_required
def crear_sorteo(request):
    productos = Producto.objects.filter(stock__gt=0)
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        producto = get_object_or_404(Producto, id=producto_id)
        if Sorteo.objects.filter(producto=producto, cerrado=False).exists():
            messages.error(request, "Ya existe un sorteo activo para este producto.")
            return redirect("crear_sorteo")
        else:
            producto_id = request.POST.get("producto_id")
            if producto_id:
                producto = get_object_or_404(Producto, id=producto_id)
                Sorteo.objects.create(producto=producto)
                messages.success(
                    request,
                    f"El sorteo de un {producto.descripcion} de {producto.nombre} ha sido publicado.",
                )
                return redirect("sorteo_admin")
            else:
                messages.error(request, "Se requiere un empleado para crear el sorteo.")
                return redirect("crear_sorteo")
    return render(
        request, "components/app_sorteo/crear_sorteo.html", {"productos": productos}
    )


@login_required
@staff_member_required
def cerrar_sorteo(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    sorteo = Sorteo.objects.filter(producto=producto, cerrado=False).first()
    if not sorteo:
        messages.error(
            request, "No hay un sorteo activo para este producto o ya ha sido cerrado."
        )
        return redirect("sorteos")

    participaciones = Participacion.objects.filter(sorteo=sorteo)

    if request.method == "POST":
        if participaciones.exists():
            with transaction.atomic():
                # Seleccionar un ganador
                ganador = random.choice(participaciones)

                # Cerrar el sorteo y guardar el resultado
                sorteo.cerrado = True
                sorteo.resultado = True
                sorteo.save()

                # Reducir el stock del producto
                producto.stock -= 1
                producto.save()

                # Crear una OrdenPedido para el ganador
                orden = OrdenPedido.objects.create(
                    empleado=ganador.empleado.usuario,  # Usuario ganador
                    razon_social = ganador.empleado,
                    estado="Aprobada",  # Estado de la orden
                    total_puntos=producto.puntos_requeridos // 2,  # Asumiendo que el producto tiene un campo 'puntos'
                )

                # Crear un ProductoCanjeado asociado a la OrdenPedido
                ProductoCanjeado.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad=1,  # Solo se está sorteando un producto
                    puntos_gastados=producto.puntos_requeridos // 2,  # Puntos que costaría el producto
                )

                # Notificar al ganador
                ganador_usuario = ganador.empleado.usuario
                send_mail(
                    "¡Felicidades! Has ganado el sorteo",
                    f"Hola {ganador_usuario.get_full_name()},\n\n"
                    "¡Felicitaciones! Has ganado el sorteo del producto "
                    f"{producto.nombre}. Tu orden ha sido creada "
                    "y pronto recibirás tu comprobante.\n\nGracias por participar.",
                    settings.DEFAULT_FROM_EMAIL,
                    [ganador_usuario.email],  # Correo electrónico del ganador
                    fail_silently=False,
                )
            messages.success(
                request,
                f"El sorteo ha sido cerrado. El ganador es {ganador_usuario.get_full_name()}. Se ha notificado al ganador y creado una orden de compra.",
            )
            return redirect("sorteo_admin")
        else:
            messages.error(
                request,
                "No se puede cerrar el sorteo porque no hay participaciones.",
            )
            return redirect("sorteo_admin")

    context = {
        "sorteo": sorteo,
        "participaciones": participaciones,
    }

    return render(request, "components/app_sorteo/cerrar_sorteo.html", context)


@login_required
def leer_sorteo(request):
    empleado = get_object_or_404(Empleado, usuario=request.user)
    sorteo_activo = Sorteo.objects.filter(cerrado=False).first()

    if sorteo_activo:
        # Filtra las participaciones que pertenecen al sorteo activo
        participaciones = Participacion.objects.filter(sorteo=sorteo_activo)
        producto = sorteo_activo.producto
        context = {
            "participaciones": participaciones,
            "empleado": empleado,
            "producto": producto,
            "sorteo": sorteo_activo,
        }
    else:
        context = {
            "empleado": empleado,
            "sorteo": None,
        }

    return render(request, "components/app_sorteo/participar.html", context)


@login_required
def participar_sorteo(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    empleado = get_object_or_404(Empleado, usuario=request.user)

    # Usar la mitad de los puntos requeridos para participar
    puntos_requeridos = producto.puntos_requeridos // 2

    sorteo = Sorteo.objects.filter(producto=producto, cerrado=False).first()
    if not sorteo:
        messages.error(request, "No hay un sorteo activo para este producto.")
        return redirect("sorteos")

    # Verificar si el empleado tiene suficientes puntos (mitad de los puntos requeridos)
    if empleado.puntos < puntos_requeridos:
        messages.error(
            request, "No tienes suficientes puntos para participar en este sorteo."
        )
        return redirect("sorteos")

    # Verificar si ya ha participado
    if Participacion.objects.filter(sorteo=sorteo, empleado=empleado).exists():
        messages.error(request, "Ya has participado en este sorteo.")
        return redirect("sorteos")

    if request.method == "POST":
        with transaction.atomic():
            # Reducir los puntos del empleado (mitad de los puntos requeridos)
            empleado.puntos -= puntos_requeridos
            empleado.save()

            # Crear la participación en el sorteo
            Participacion.objects.create(sorteo=sorteo, empleado=empleado)

        messages.success(request, "Has participado en el sorteo exitosamente.")
        return redirect("sorteos")

    return render(request, "components/app_sorteo/sorteo.html", {"producto": producto})
