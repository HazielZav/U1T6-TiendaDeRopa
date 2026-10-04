from django.db import migrations

def crear_cliente_publico(apps, schema_editor):
    Cliente = apps.get_model('tienda', 'Cliente')
    Cliente.objects.get_or_create(
        nombre='Público',
        apellidos='general'
    )

class Migration(migrations.Migration):
    dependencies = [
        ('tienda', '0002_alter_cliente_id_alter_color_id_and_more'),
    ]

    operations = [
        migrations.RunPython(crear_cliente_publico),
    ]
