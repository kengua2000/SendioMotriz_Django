from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils import timezone

class RolChoices(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    VENDEDOR = 'Vendedor', 'Vendedor'
    CLIENTE = 'Cliente', 'Cliente'
    EMPLEADO = 'Empleado', 'Empleado'

class EstadoProductoChoices(models.TextChoices):
    DISPONIBLE = 'Disponible', 'Disponible'
    AGOTADO = 'Agotado', 'Agotado'


class MetodoPagoChoices(models.TextChoices):
    EFECTIVO = 'Efectivo', 'Efectivo'
    TARJETA = 'Tarjeta', 'Tarjeta'
    TRANSFERENCIA = 'Transferencia', 'Transferencia'

class EstadoPagoChoices(models.TextChoices):
    PENDIENTE = 'Pendiente', 'Pendiente'
    COMPLETADO = 'Completado', 'Completado'
    CANCELADO = 'Cancelado', 'Cancelado'

class Cliente(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=20, validators=[MinLengthValidator(8)])
    rol = models.CharField(
        max_length=20,
        choices=RolChoices.choices,
        default=RolChoices.CLIENTE
    )
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.cedula}"

class Empleado(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=20, validators=[MinLengthValidator(8)])
    rol = models.CharField(
        max_length=20,
        choices=RolChoices.choices,
        default=RolChoices.EMPLEADO
    )
    telefono = models.CharField(max_length=15, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.cedula}"
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto_nombre = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo_electronico = models.EmailField(unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=50)
    imagen = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=EstadoProductoChoices.choices,
        default=EstadoProductoChoices.DISPONIBLE
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='productos'
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"
    
class Vehiculo(models.Model):
    class EstadoVehiculoChoices(models.TextChoices):
        DISPONIBLE = 'Disponible', 'Disponible'
        AGOTADO = 'Agotado', 'Agotado'

    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    color = models.CharField(max_length=50)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])
    imagen = models.TextField(blank=True, null=True)
    km_recorridos = models.IntegerField(validators=[MinValueValidator(0)])
    tipo_combustible = models.CharField(max_length=50)
    estado = models.CharField(
        max_length=20,
        choices=EstadoVehiculoChoices.choices,
        default=EstadoVehiculoChoices.DISPONIBLE
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehiculos'
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"


class Factura(models.Model):
    empleado = models.CharField(max_length=100, unique=True) # Mantén esta relación si la tabla Empleado existe
    cliente = models.CharField(max_length=100, unique=True)
    fecha = models.DateField(default=timezone.now)  # Cambiado a `fecha` como en el código inicial
    hora = models.TimeField(default=timezone.now)  # Agregado el campo `hora`
    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ('efectivo', 'Efectivo'),
            ('tarjeta', 'Tarjeta'),
            ('transferencia', 'Transferencia')
        ],  # Ajustando los métodos de pago
        default='efectivo'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"Factura #{self.id} - {self.cliente}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        'Producto',  # Asume que existe un modelo Producto
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='detalles_factura'
    )
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def save(self, *args, **kwargs):
        # Asegura que la factura esté validada correctamente
        if not self.producto:
            raise ValueError('Debe especificar un producto para el detalle.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de {self.producto} en Factura #{self.factura.id}"


