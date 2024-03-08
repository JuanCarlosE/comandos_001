# Generated by Django 4.2.3 on 2024-03-07 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Soldier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=100, verbose_name='Nombres:')),
                ('lastNames', models.CharField(max_length=100, verbose_name='Apellidos:')),
                ('rh', models.CharField(blank=True, max_length=3, verbose_name='RH:')),
                ('age', models.SmallIntegerField(verbose_name='Edad:')),
                ('phoneNumber', models.CharField(max_length=20, unique=True, verbose_name='No. celular:')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email:')),
                ('userPhoto', models.ImageField(blank=True, upload_to='photos/', verbose_name='Foto:')),
                ('notes', models.TextField(blank=True, verbose_name='Observaciones:')),
            ],
            options={
                'verbose_name': 'Soldado',
                'verbose_name_plural': 'Soldados',
            },
        ),
        migrations.CreateModel(
            name='Measures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='Peso:')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='Altura:')),
                ('shoulders', models.FloatField(blank=True, null=True, verbose_name='Hombros:')),
                ('abds', models.FloatField(blank=True, null=True, verbose_name='Abdomen:')),
                ('pectoral', models.FloatField(blank=True, null=True, verbose_name='Pectorales:')),
                ('leftBicep', models.FloatField(blank=True, null=True, verbose_name='Bicep izquierdo:')),
                ('rightBicep', models.FloatField(blank=True, null=True, verbose_name='Bicep derecho:')),
                ('leftForearm', models.FloatField(blank=True, null=True, verbose_name='Antebrazo izquierdo:')),
                ('rightForearm', models.FloatField(blank=True, null=True, verbose_name='Antebrazo derecho:')),
                ('leftLeg', models.FloatField(blank=True, null=True, verbose_name='Pierna izquierda:')),
                ('RightLeg', models.FloatField(blank=True, null=True, verbose_name='Pierna derecha:')),
                ('neck', models.FloatField(blank=True, null=True, verbose_name='Cuello:')),
                ('ass', models.FloatField(blank=True, null=True, verbose_name='Gluteo:')),
                ('soldier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soldiers.soldier')),
            ],
            options={
                'verbose_name': 'Medida',
                'verbose_name_plural': 'Medidas',
            },
        ),
        migrations.CreateModel(
            name='Assistence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerDate', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='Estado')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Factura:')),
                ('soldier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soldiers.soldier', verbose_name='Soldado:')),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
            },
        ),
    ]
