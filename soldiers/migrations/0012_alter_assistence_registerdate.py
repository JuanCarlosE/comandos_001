# Generated by Django 4.2.3 on 2023-12-15 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soldiers', '0011_alter_assistence_registerdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistence',
            name='registerDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
