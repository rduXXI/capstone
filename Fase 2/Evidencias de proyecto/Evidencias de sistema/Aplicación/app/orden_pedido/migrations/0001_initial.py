# Generated by Django 5.1.2 on 2024-10-20 18:28

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
            name='OrdenPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('total_puntos', models.IntegerField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordenes_pedido', to='roles.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoCanjeado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('puntos_gastados', models.IntegerField()),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_canjeados', to='orden_pedido.ordenpedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
    ]
