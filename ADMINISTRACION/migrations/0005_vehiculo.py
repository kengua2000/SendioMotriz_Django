# Generated by Django 5.1.2 on 2024-11-25 00:56

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADMINISTRACION', '0004_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=20, unique=True)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('color', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('imagen', models.TextField(blank=True, null=True)),
                ('km_recorridos', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('tipo_combustible', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('Disponible', 'Disponible'), ('Agotado', 'Agotado')], default='Disponible', max_length=20)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehiculos', to='ADMINISTRACION.proveedor')),
            ],
        ),
    ]