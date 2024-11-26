from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from ADMINISTRACION.models import Producto, Vehiculo

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password  # Para verificar contraseñas hasheadas (opcional)
from ADMINISTRACION.models import Cliente, Empleado  # Importar los modelos personalizados

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Puede ser correo o cédula
        password = request.POST.get('password')

        # Intentar autenticación en la tabla de clientes
        try:
            user = Cliente.objects.get(Q(cedula=username) | Q(correo_electronico=username))
            if password == user.contrasena:  # Verificar contraseña hasheada
                request.session['user_id'] = user.id
                request.session['user_role'] = 'cliente'
                request.session['username'] = user.nombre_completo
                request.session['email'] = user.correo_electronico
                return redirect('home')  # Página principal para clientes
        except Cliente.DoesNotExist:
            pass

        # Intentar autenticación en la tabla de empleados
        try:
            user = Empleado.objects.get(Q(cedula=username) | Q(correo_electronico=username))
            if password == user.contrasena:  # Verificar contraseña hasheada
                request.session['user_id'] = user.id
                request.session['user_role'] = 'empleado'
                request.session['username'] = user.nombre_completo
                request.session['email'] = user.correo_electronico
                return redirect('/administracion/')  # Página principal para empleados
        except Empleado.DoesNotExist:
            pass

        # Si no se encontró en ninguna tabla
        messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login2.html')


def home(request):
    if 'user_id' in request.session:
        # Usuario autenticado
        username = request.session.get('username')
        user_role = request.session.get('user_role')
        if user_role == 'cliente':
            # Renderiza la página principal con el nombre del cliente
            return render(request, 'vista.html', {'username': username})
        elif user_role == 'empleado':
            # Redirige al área de administración si es empleado
            return redirect('/administracion/')
    else:
        # Usuario no autenticado: Renderiza la página principal sin datos de sesión
        return render(request, 'vista.html')
    
def acercadenosotros(request):
    return render(request, 'acerca.html')

    
def logout(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return render(request, 'vista.html')



def lista_productos2(request):
    # Obtener el término de búsqueda de la solicitud
    query = request.GET.get('busqueda', '')
    
    # Filtrar productos por nombre o marca que coincidan con la búsqueda
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(marca__icontains=query)
        )
    else:
        productos = Producto.objects.all()
    
    return render(request, 'productos/productos.html', {
        'productos': productos, 
        'busqueda': query  # Pasar el término de búsqueda de vuelta a la plantilla
    })

def lista_vehiculos2(request):
    # Obtener el término de búsqueda de la solicitud
    query = request.GET.get('busqueda', '')
    
    # Filtrar vehículos por marca, modelo, placa o color
    if query:
        vehiculos = Vehiculo.objects.filter(
            Q(marca__icontains=query) | 
            Q(modelo__icontains=query) | 
            Q(placa__icontains=query) | 
            Q(color__icontains=query)
        )
    else:
        vehiculos = Vehiculo.objects.all()
    
    return render(request, 'vehiculos/vehiculos.html', {
        'vehiculos': vehiculos, 
        'busqueda': query  # Pasar el término de búsqueda de vuelta a la plantilla
    })


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto
    })

def detalle_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    return render(request, 'vehiculos/detalle_vehiculo.html', {
        'vehiculo': vehiculo
    })