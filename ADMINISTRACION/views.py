from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm

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
    if id:
        cliente = get_object_or_404(Cliente, id=id)
        title = "Actualizar Cliente"
    else:
        cliente = None
        title = "Crear Cliente"

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')  # Redirigir a la lista de clientes después de guardar
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'administracion/clientes/cliente_form.html', {'form': form, 'title': title})


# Eliminar Cliente
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_clientes') 
