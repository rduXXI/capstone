from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from . import models


@login_required
def categoria(request):
    categorias = models.Categoria.objects.all().order_by("nombre")
    context = {
        "categorias": categorias,
    }
    return render(request, "components/productos/leer_categorias.html", context)


@login_required
def marca(request):
    marcas = models.Marca.objects.all().order_by("nombre")
    context = {
        "marcas": marcas,
    }
    return render(request, "components/productos/leer_marcas.html", context)


@login_required
def procedencia(request):
    procedencias = models.Procedencia.objects.all().order_by("codigo_iso")
    context = {
        "procedencias": procedencias,
    }
    return render(request, "components/productos/leer_procedencias.html", context)


@login_required
def producto(request):
    productos = models.Producto.objects.all().order_by("categoria__nombre", "nombre")
    context = {
        "productos": productos,
    }
    return render(request, "components/productos/leer_productos.html", context)


@login_required
def proveedor(request):
    proveedores = models.Proveedor.objects.all()
    context = {
        "proveedores": proveedores,
    }
    return render(request, "components/productos/leer_proveedores.html", context)


@login_required
def add_categoria(request):
    if request.method == "POST":
        form = forms.CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guardado correctamente en la base de datos")
            return redirect("categorias")
    else:
        form = forms.CategoriaForm()
    context = {
        "form": form,
    }
    return render(request, "components/productos/crear_categoria.html", context)


@login_required
def add_marca(request):
    if request.method == "POST":
        form = forms.MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guardado correctamente en la base de datos")
            return redirect("marcas")
    else:
        form = forms.MarcaForm()
    context = {
        "form": form,
    }
    return render(request, "components/productos/crear_marca.html", context)


@login_required
def add_procedencia(request):
    if request.method == "POST":
        form = forms.ProcedenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guardado correctamente en la base de datos")
            return redirect("procedencias")
    else:
        form = forms.ProcedenciaForm()
    context = {
        "form": form,
    }
    return render(request, "components/productos/crear_procedencia.html", context)


@login_required
def add_producto(request):
    if request.method == "POST":
        form = forms.ProductoForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "El producto " + form.cleaned_data["nombre"] + " ha sido agregado correctamente.")
            return redirect("productos")
    else:
        form = forms.ProductoForm()
    context = {"form": form}
    return render(request, "components/productos/crear_producto.html", context)


@login_required
def add_proveedor(request):
    if request.method == "POST":
        form = forms.ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guardado correctamente en la base de datos")
            return redirect("proveedores")
    else:
        form = forms.ProveedorForm()  # Initialize the form if the method is not POST
    context = {
        "form": form,
    }
    return render(request, "components/productos/crear_proveedor.html", context)
