# Generated by Django 5.1.2 on 2024-11-24 17:54

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADMINISTRACION', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('correo_electronico', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(8)])),
                ('rol', models.CharField(choices=[('Admin', 'Admin'), ('Vendedor', 'Vendedor'), ('Cliente', 'Cliente'), ('Empleado', 'Empleado')], default='Empleado', max_length=20)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]