# Generated by Django 5.0.3 on 2024-05-16 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magna_app', '0005_remove_usuario_last_login_remove_usuario_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='tipo_de_cuota',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='magna_app.tipocuota'),
            preserve_default=False,
        ),
    ]
