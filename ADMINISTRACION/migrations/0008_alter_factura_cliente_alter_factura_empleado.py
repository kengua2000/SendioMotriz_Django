# Generated by Django 5.1.2 on 2024-11-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADMINISTRACION', '0007_remove_detallefactura_vehiculo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='cliente',
            field=models.CharField(default='Desconocido', max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factura',
            name='empleado',
            field=models.CharField(default='Desconocido', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
