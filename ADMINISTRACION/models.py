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

