from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from autenticacion.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from roles.models import Empleado

def cerrar_sesion(request):
    logout(request)
    
    return redirect('home')

@login_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)

            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def listado_usuarios(request):
    empleados = Empleado.objects.all()
    usuarios = User.objects.all()
    
    context = {
        'empleados': empleados,
        'usuarios': usuarios,
    }
    
    return render(request, 'components/listado_usuarios.html', context)