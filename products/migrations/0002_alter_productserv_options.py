# Generated by Django 4.2.3 on 2023-11-29 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productserv',
            options={'verbose_name': 'Producto/Servicio', 'verbose_name_plural': 'Productos/Servicios'},
        ),
    ]