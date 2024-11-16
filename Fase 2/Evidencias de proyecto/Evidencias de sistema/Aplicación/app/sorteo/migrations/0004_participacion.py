# Generated by Django 5.1.2 on 2024-10-19 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_delete_rol'),
        ('sorteo', '0003_alter_sorteo_empleado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_participacion', models.DateTimeField(auto_now_add=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roles.empleado')),
                ('sorteo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sorteo.sorteo')),
            ],
        ),
    ]
