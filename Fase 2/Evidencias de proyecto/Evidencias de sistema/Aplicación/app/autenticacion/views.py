from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from autenticacion.forms import CustomUserCreationForm
from roles.models import Empleado


def cerrar_sesion(request):
    logout(request)

    return redirect("login")


@transaction.atomic
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Asignación del grupo
                group = form.cleaned_data.get("group")
                if group:
                    group.user_set.add(user)

                messages.success(request, "Guardado correctamente en la base de datos.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Error al registrar el usuario: {str(e)}")
                return render(request, "registration/register.html", {"form": form})
        else:
            messages.error(request, "Hubo un error al registrar el usuario. Por favor, revisa los campos.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def listado_usuarios(request):
    empleados = Empleado.objects.all()
    usuarios = User.objects.all()

    context = {
        "empleados": empleados,
        "usuarios": usuarios,
    }

    return render(request, "components/listado_usuarios.html", context)
