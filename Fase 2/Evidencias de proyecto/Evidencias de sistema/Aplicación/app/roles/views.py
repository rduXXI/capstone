from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from roles.forms import EmpleadoForm, PuntosForm
from roles.models import Empleado

@login_required
def asignar_puntos(request, id=None):
    if id:
        empleado = get_object_or_404(Empleado, id=id)
    else:
        empleado = None

    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if formulario.is_valid():
            formulario.save()
            datos = {
                'mensaje': "Guardado correctamente",
                'form': formulario
            }
            return redirect('listado_usuarios')
        else:
            datos = {
                'form': formulario
            }
    else:
        formulario = EmpleadoForm(instance=empleado)
        datos = {
            'form': formulario
        }
    
    return render(request, 'components/asignar_puntos.html', datos)

@login_required
def crear_puntos(request):
    if request.method == 'POST':
        form = PuntosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_usuarios')
    else:
        form = PuntosForm()
    return render(request, 'components/asignar_puntos.html', {'form': form})

def view_puntos(request):
    if request.user.is_authenticated:
        empleado = Empleado.objects.get(Empleado, usuario=request.user)
        
    return render(request, 'components/catalogo.html', {'puntos': empleado.puntos})