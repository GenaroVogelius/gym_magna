# Generated by Django 5.0.6 on 2024-05-26 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magna_app', '0017_remove_precioshistorico_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='dia',
            field=models.DateField(),
        ),
    ]
