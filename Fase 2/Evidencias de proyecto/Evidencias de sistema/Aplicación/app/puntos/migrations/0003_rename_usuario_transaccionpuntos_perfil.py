# Generated by Django 5.1.2 on 2024-10-18 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puntos', '0002_rename_created_at_transaccionpuntos_creado_en_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaccionpuntos',
            old_name='usuario',
            new_name='perfil',
        ),
    ]
