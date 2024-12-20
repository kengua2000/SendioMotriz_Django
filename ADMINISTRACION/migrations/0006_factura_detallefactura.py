# Generated by Django 5.1.2 on 2024-11-25 02:31

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADMINISTRACION', '0005_vehiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateTimeField(default=django.utils.timezone.now)),
                ('metodo_pago', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Tarjeta', 'Tarjeta'), ('Transferencia', 'Transferencia')], max_length=20)),
                ('estado_pago', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Completado', 'Completado'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facturas', to='ADMINISTRACION.cliente')),
                ('empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facturas', to='ADMINISTRACION.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detalles_factura', to='ADMINISTRACION.producto')),
                ('vehiculo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detalles_factura', to='ADMINISTRACION.vehiculo')),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ADMINISTRACION.factura')),
            ],
        ),
    ]
