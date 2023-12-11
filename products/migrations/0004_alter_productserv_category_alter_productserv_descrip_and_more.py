# Generated by Django 4.2.3 on 2023-12-11 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productserv_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productserv',
            name='category',
            field=models.CharField(choices=[('PROD', 'Producto'), ('SERV', 'Servicio'), ('SUBS', 'Suscripción ')], default='SUBS', max_length=4, verbose_name='Categoría:'),
        ),
        migrations.AlterField(
            model_name='productserv',
            name='descrip',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción:'),
        ),
        migrations.AlterField(
            model_name='productserv',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Nombre:'),
        ),
        migrations.AlterField(
            model_name='productserv',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Precio:'),
        ),
        migrations.AlterField(
            model_name='productserv',
            name='status',
            field=models.BooleanField(verbose_name='Estado'),
        ),
    ]