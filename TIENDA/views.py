from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from ADMINISTRACION.models import Producto, Vehiculo

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/administracion/')  # Redirige a la página principal después del login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login2.html')

def home(request):
    return render(request, 'vista.html')


def lista_productos2(request):
    productos = Producto.objects.all()  # Trae todos los productos
    return render(request, 'productos.html', {'productos': productos})

def lista_vehiculos2(request):
    vehiculos = Vehiculo.objects.all()  # Trae todos los vehículos
    return render(request, 'vehiculos.html', {'vehiculos': vehiculos})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'detalle_producto.html', {
        'producto': producto
    })

def detalle_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    return render(request, 'detalle_vehiculo.html', {
        'vehiculo': vehiculo
    })