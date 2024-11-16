# Generated by Django 5.1.2 on 2024-10-22 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0005_rename_paisorigen_procedencia_and_more'),
        ('roles', '0004_delete_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subasta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('estado', models.CharField(default='Activa', max_length=20)),
                ('ganador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subastas_ganadas', to='roles.empleado')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subastas', to='productos.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Puja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntos_ofrecidos', models.PositiveIntegerField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pujas', to='roles.empleado')),
                ('subasta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pujas', to='subasta.subasta')),
            ],
        ),
    ]
