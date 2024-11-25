
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Cliente, Empleado, Producto, Proveedor, Vehiculo
from .forms import ClienteForm, EmpleadoForm, ProductoForm, ProveedorForm, VehiculoForm

from django.contrib import messages
from django.core.exceptions import ValidationError


from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def home_administracion(request):
    # Obtener conteos de cada modelo
    clientes_count = Cliente.objects.count()
    
    
    context = {
        'clientes_count': clientes_count,
        
    }
    return render(request, 'administracion/administracion.html', context)

# Lista de Clientes
def lista_clientes(request):
    query = request.GET.get('q', '')  # Obtén el valor de búsqueda, si existe
    clientes = Cliente.objects.all()
    
    if query:
        clientes = clientes.filter(
            Q(cedula__icontains=query) |
            Q(nombre_completo__icontains=query) |
            Q(correo_electronico__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query)  # Cambié "celular" por "telefono" para coincidir con tu modelo
        )

    context = {
        'clientes': clientes,
        'query': query,
    }
    return render(request, 'administracion/clientes/lista.html', context)

# Crear o Editar Cliente
def crear_o_editar_cliente(request, id=None):
    try:
        if id:
            cliente = get_object_or_404(Cliente, id=id)
            title = "Actualizar Cliente"
        else:
            cliente = None
            title = "Crear Cliente"

        if request.method == 'POST':
            form = ClienteForm(request.POST, instance=cliente)
            
            if form.is_valid():
                try:
                    cliente = form.save()
                    messages.success(request, 'Cliente guardado exitosamente.')
                    return redirect('lista_clientes')
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        if 'cedula' in str(e).lower():
                            form.add_error('cedula', 'Ya existe un cliente con esta cédula.')
                        elif 'correo_electronico' in str(e).lower():
                            form.add_error('correo_electronico', 'Ya existe un cliente con este correo electrónico.')
            else:
                # Agregar mensajes de error específicos para cada campo
                for field_name, error_list in form.errors.items():
                    field_label = form.fields[field_name].label or field_name
                    for error in error_list:
                        messages.add_message(request, messages.ERROR, f'Error en {field_label}: {error}')

        else:
            form = ClienteForm(instance=cliente)

        context = {
            'form': form,
            'title': title,
            'cliente': cliente,
            'is_edit': bool(id)
        }

        return render(request, 'administracion/clientes/cliente_form.html', context)

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Error al procesar la solicitud: {str(e)}')
        return redirect('lista_clientes')


# Eliminar Cliente
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_clientes') 


# Lista de Empleados
def lista_empleados(request):
    query = request.GET.get('q', '')  # Obtén el valor de búsqueda, si existe
    empleados = Empleado.objects.all()
    
    if query:
        empleados = empleados.filter(
            Q(cedula__icontains=query) |
            Q(nombre_completo__icontains=query) |
            Q(correo_electronico__icontains=query) |
            Q(telefono__icontains=query)  # Filtro por teléfono
        )

    context = {
        'empleados': empleados,
        'query': query,
    }
    return render(request, 'administracion/empleados/lista.html', context)

# Crear o Editar Empleado
def crear_o_editar_empleado(request, id=None):
    try:
        if id:
            empleado = get_object_or_404(Empleado, id=id)
            title = "Actualizar Empleado"
        else:
            empleado = None
            title = "Crear Empleado"

        if request.method == 'POST':
            form = EmpleadoForm(request.POST, instance=empleado)
            
            if form.is_valid():
                try:
                    empleado = form.save()
                    messages.success(request, 'Empleado guardado exitosamente.')
                    return redirect('lista_empleados')
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        if 'cedula' in str(e).lower():
                            form.add_error('cedula', 'Ya existe un empleado con esta cédula.')
                        elif 'correo_electronico' in str(e).lower():
                            form.add_error('correo_electronico', 'Ya existe un empleado con este correo electrónico.')
            else:
                # Agregar mensajes de error específicos para cada campo
                for field_name, error_list in form.errors.items():
                    field_label = form.fields[field_name].label or field_name
                    for error in error_list:
                        messages.add_message(request, messages.ERROR, f'Error en {field_label}: {error}')

        else:
            form = EmpleadoForm(instance=empleado)

        context = {
            'form': form,
            'title': title,
            'empleado': empleado,
            'is_edit': bool(id)
        }

        return render(request, 'administracion/empleados/empleado_form.html', context)

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Error al procesar la solicitud: {str(e)}')
        return redirect('lista_empleados')


# Eliminar Empleado
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    messages.success(request, 'Empleado eliminado exitosamente.')
    return redirect('lista_empleados')


def lista_proveedores(request):
    query = request.GET.get('q', '')  # Término de búsqueda
    proveedores = Proveedor.objects.all()

    if query:
        proveedores = proveedores.filter(
            Q(nombre__icontains=query) |
            Q(contacto_nombre__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo_electronico__icontains=query)
        )

    context = {
        'proveedores': proveedores,
        'query': query,
    }
    return render(request, 'administracion/proveedores/lista.html', context)

# Crear o Editar Proveedor
def crear_o_editar_proveedor(request, id=None):
    try:
        if id:
            proveedor = get_object_or_404(Proveedor, id=id)
            title = "Actualizar Proveedor"
        else:
            proveedor = None
            title = "Crear Proveedor"

        if request.method == 'POST':
            form = ProveedorForm(request.POST, instance=proveedor)

            if form.is_valid():
                try:
                    proveedor = form.save()
                    messages.success(request, f'Proveedor "{proveedor.nombre}" guardado exitosamente.')
                    return redirect('lista_proveedores')
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        if 'correo_electronico' in str(e).lower():
                            form.add_error('correo_electronico', 'Ya existe un proveedor con este correo electrónico.')
            else:
                # Agregar mensajes de error específicos para cada campo
                for field_name, error_list in form.errors.items():
                    field_label = form.fields[field_name].label or field_name
                    for error in error_list:
                        messages.add_message(request, messages.ERROR, f'Error en {field_label}: {error}')

        else:
            form = ProveedorForm(instance=proveedor)

        context = {
            'form': form,
            'title': title,
            'proveedor': proveedor,
            'is_edit': bool(id),
        }

        return render(request, 'administracion/proveedores/proveedor_form.html', context)

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Error al procesar la solicitud: {str(e)}')
        return redirect('lista_proveedores')

# Eliminar Proveedor
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    proveedor.delete()
    messages.success(request, f'Proveedor "{proveedor.nombre}" eliminado exitosamente.')
    return redirect('lista_proveedores')

def lista_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.all()
    
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(color__icontains=query) |
            Q(estado__icontains=query) |
            Q(proveedor__nombre__icontains=query)  # Asumiendo que el proveedor tiene un campo nombre
        )
    
    # Ordenar productos por fecha de creación, más recientes primero
    productos = productos.order_by('-fecha_creacion')

    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'administracion/productos/lista.html', context)

def crear_o_editar_producto(request, id=None):
    try:
        if id:
            producto = get_object_or_404(Producto, id=id)
            title = "Actualizar Producto"
        else:
            producto = None
            title = "Crear Producto"

        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto)
            
            if form.is_valid():
                try:
                    producto = form.save()
                    messages.success(request, 'Producto guardado exitosamente.')
                    return redirect('lista_productos')
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower():
                        if 'nombre' in str(e).lower():
                            form.add_error('nombre', 'Ya existe un producto con este nombre.')
                        # Agregar más validaciones de unicidad si son necesarias
            else:
                # Agregar mensajes de error específicos para cada campo
                for field_name, error_list in form.errors.items():
                    field_label = form.fields[field_name].label or field_name
                    for error in error_list:
                        messages.add_message(request, messages.ERROR, f'Error en {field_label}: {error}')

        else:
            form = ProductoForm(instance=producto)

        context = {
            'form': form,
            'title': title,
            'producto': producto,
            'is_edit': bool(id)
        }

        return render(request, 'administracion/productos/producto_form.html', context)

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Error al procesar la solicitud: {str(e)}')
        return redirect('lista_productos')
# Eliminar Producto
def eliminar_producto(request, id):
    try:
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar el producto: {str(e)}')
    return redirect('lista_productos')

# Listar Vehículos
def lista_vehiculos(request):
    query = request.GET.get('q', '')
    vehiculos = Vehiculo.objects.all()

    if query:
        vehiculos = vehiculos.filter(
            Q(placa__icontains=query) |
            Q(marca__icontains=query) |
            Q(modelo__icontains=query) |
            Q(color__icontains=query) |
            Q(estado__icontains=query) |
            Q(proveedor__nombre__icontains=query)  # Asumiendo que proveedor tiene un campo nombre
        )

    # Ordenar vehículos por fecha de creación, más recientes primero
    vehiculos = vehiculos.order_by('-fecha_creacion')

    context = {
        'vehiculos': vehiculos,
        'query': query,
    }
    return render(request, 'administracion/vehiculos/lista.html', context)

# Crear o Editar Vehículo
def crear_o_editar_vehiculo(request, id=None):
    try:
        if id:
            vehiculo = get_object_or_404(Vehiculo, id=id)
            title = "Actualizar Vehículo"
        else:
            vehiculo = None
            title = "Crear Vehículo"

        if request.method == 'POST':
            form = VehiculoForm(request.POST, instance=vehiculo)

            if form.is_valid():
                try:
                    # Guardar el vehículo
                    vehiculo = form.save()

                    messages.success(request, 'Vehículo guardado exitosamente.')
                    return redirect('lista_vehiculos')
                except IntegrityError as e:
                    # Verificar el error de duplicado solo si la placa es nueva
                    if 'unique constraint' in str(e).lower():
                        if 'placa' in str(e).lower():
                            # Verificar si el vehículo que estamos actualizando tiene la misma placa
                            if vehiculo and vehiculo.placa == form.cleaned_data['placa']:
                                messages.error(request, 'La placa no se ha modificado y sigue siendo válida.')
                            else:
                                form.add_error('placa', 'Ya existe un vehículo con esta placa.')
                        # Agregar más validaciones de unicidad si son necesarias
            else:
                # Agregar mensajes de error específicos para cada campo
                for field_name, error_list in form.errors.items():
                    field_label = form.fields[field_name].label or field_name
                    for error in error_list:
                        messages.add_message(request, messages.ERROR, f'Error en {field_label}: {error}')

        else:
            form = VehiculoForm(instance=vehiculo)

        context = {
            'form': form,
            'title': title,
            'vehiculo': vehiculo,
            'is_edit': bool(id)
        }

        return render(request, 'administracion/vehiculos/vehiculo_form.html', context)

    except Exception as e:
        messages.add_message(request, messages.ERROR, f'Error al procesar la solicitud: {str(e)}')
        return redirect('lista_vehiculos')

# Eliminar Vehículo
def eliminar_vehiculo(request, id):
    try:
        vehiculo = get_object_or_404(Vehiculo, id=id)
        vehiculo.delete()
        messages.success(request, f'Vehículo con placa "{vehiculo.placa}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar el vehículo: {str(e)}')
    return redirect('lista_vehiculos')






