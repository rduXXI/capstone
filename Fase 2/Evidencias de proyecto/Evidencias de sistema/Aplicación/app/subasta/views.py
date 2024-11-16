from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from orden_pedido.models import OrdenPedido, ProductoCanjeado
from subasta.forms import SubastaForm
from .models import Empleado, Puja, Subasta


def subasta(request):
    subastas = Subasta.objects.filter(estado="Activa").first()
    empleado = Empleado.objects.get(usuario=request.user)
    pujas = Puja.objects.filter(subasta=subastas).order_by("-puntos_ofrecidos")
    context = {
        "empleado": empleado,
        "subastas": subastas,
        "pujas": pujas,
    }
    return render(request, "components/app_subasta/lista_subastas.html", context)


def pujar(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)
    empleado = get_object_or_404(Empleado, usuario=request.user)

    if subasta.estado != "Activa":
        messages.error(request, "Esta subasta ya no está activa.")
        return redirect("lista_subastas")

    if request.method == "POST":
        puntos_ofrecidos = int(request.POST["puntos_ofrecidos"])

        if empleado.puntos_subasta >= puntos_ofrecidos:
            # Buscar si ya existe una puja del empleado en esta subasta
            puja_existente = Puja.objects.filter(
                subasta=subasta, empleado=empleado
            ).first()

            if puja_existente:
                # Si existe una puja, sumamos los puntos ofrecidos a la puja existente
                puja_existente.puntos_ofrecidos += puntos_ofrecidos
                puja_existente.save()
                messages.success(request, "Has aumentado tu puja correctamente.")
            else:
                # Si no existe una puja, creamos una nueva
                Puja.objects.create(
                    subasta=subasta,
                    empleado=empleado,
                    puntos_ofrecidos=puntos_ofrecidos,
                )
                messages.success(request, "Has pujado correctamente.")

            # Restar los puntos del empleado
            empleado.puntos_subasta -= puntos_ofrecidos
            empleado.save()
        else:
            messages.error(request, "No tienes suficientes puntos de subasta.")

    return redirect("lista_subastas")


def historial_pujas(request):
    empleado = get_object_or_404(Empleado, usuario=request.user)
    pujas = Puja.objects.filter(empleado=empleado).order_by("-subasta__fecha_fin")
    return render(
        request, "components/app_subasta/historial_pujas.html", {"pujas": pujas}
    )


def lista_subastas_admin(request):
    subastas = Subasta.objects.all().order_by("-id")

    return render(
        request,
        "components/app_subasta/lista_subastas_admin.html",
        {"subastas": subastas},
    )


def crear_subasta(request):
    if request.method == "POST":
        form = SubastaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subasta creada exitosamente.")
            return redirect("lista_subastas_admin")
    else:
        form = SubastaForm()

    return render(request, "components/app_subasta/crear_subasta.html", {"form": form})


from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Subasta, Puja, OrdenPedido, ProductoCanjeado


def cerrar_subasta(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)

    # Verificar si la subasta está activa antes de cerrarla
    if not subasta.estado == "Activa":
        messages.error(request, "Esta subasta ya ha sido cerrada.")
        return redirect("lista_subastas_admin")

    # Obtener todas las pujas de esta subasta, ordenadas por mayor cantidad de puntos ofrecidos
    pujas = Puja.objects.filter(subasta=subasta).order_by("-puntos_ofrecidos")

    if not pujas.exists():
        messages.error(request, "No hay pujas para cerrar la subasta.")
        return redirect("lista_subastas_admin")

    # Obtener la puja ganadora (la que tiene el mayor monto)
    puja_ganadora = pujas.first()
    ganador = puja_ganadora.empleado

    # Actualizar el ganador en la subasta
    subasta.ganador = ganador
    subasta.estado = "cerrada"
    subasta.save()

    # Obtener el producto de la subasta y reducir su stock
    producto = subasta.producto
    cantidad_canjeada = 1  # Se puede ajustar si es más de una unidad subastada

    if producto.stock >= cantidad_canjeada:
        producto.stock -= cantidad_canjeada
        producto.save()
    else:
        messages.error(request, "No hay suficiente stock para el ganador.")
        return redirect("lista_subastas_admin")

    # Crear una orden de pedido para el ganador
    orden = OrdenPedido.objects.create(
        empleado=ganador.usuario,
        razon_social=ganador,  # Asigna el empleado ganador como razón social
        estado="Pendiente",
        total_puntos=puja_ganadora.puntos_ofrecidos,
    )

    # Registrar el producto canjeado en la orden de pedido
    ProductoCanjeado.objects.create(
        orden=orden,
        producto=producto,
        cantidad=cantidad_canjeada,
        puntos_gastados=puja_ganadora.puntos_ofrecidos,
    )

    # Reembolsar los puntos a los empleados que perdieron la subasta
    for puja in pujas.exclude(empleado=ganador):
        puja.empleado.puntos_subasta += puja.puntos_ofrecidos
        puja.empleado.save()

    # Enviar un correo electrónico al ganador
    send_mail(
        subject="¡Felicidades! Has ganado la subasta",
        message=(
            f"Estimado {ganador.usuario.username},\n\n"
            f"Felicitaciones por ganar la subasta de '{producto.nombre}' con {puja_ganadora.puntos_ofrecidos} puntos. "
            "Nuestro equipo procesará tu pedido pronto.\n\nGracias por participar.\nEl equipo de Subastas."
        ),
        from_email="subastas@localhost",
        recipient_list=[ganador.usuario.email],
        fail_silently=False,
    )

    messages.success(
        request,
        f"La subasta ha sido cerrada y {ganador.usuario.username} es el ganador. Se ha enviado un correo de notificación.",
    )
    return redirect("lista_subastas_admin")
