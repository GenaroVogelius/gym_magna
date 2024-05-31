# Generated by Django 5.0.3 on 2024-05-20 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magna_app', '0011_pricehistorys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricehistorys',
            name='tipo_de_plan',
        ),
        migrations.AddField(
            model_name='pricehistorys',
            name='nombre_plan',
            field=models.CharField(default='hola', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricehistorys',
            name='precio_plan',
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
    ]