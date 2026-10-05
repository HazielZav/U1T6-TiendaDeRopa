from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tienda.models import Cliente, PerfilUsuario


class Command(BaseCommand):
    help = 'Crea el cliente público y usuarios de prueba'

    def handle(self, *args, **options):
        # Crear cliente público
        cliente_publico, created = Cliente.objects.get_or_create(
            nombre='Público',
            apellidos='general'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Cliente "Público general" creado exitosamente'))
        else:
            self.stdout.write(self.style.WARNING('Cliente "Público general" ya existe'))

        # Crear usuarios de prueba
        usuarios = [
            ('admin', 'ADMIN', 'Administrador del sistema'),
            ('almacenista', 'ALMACENISTA', 'Encargado de inventario'),
            ('cajero', 'CAJERO', 'Encargado de ventas'),
        ]

        for username, rol, _ in usuarios:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'is_staff': True, 'is_superuser': True}
            )
            if created:
                user.set_password('password123')
                user.save()
                PerfilUsuario.objects.create(usuario=user, rol=rol)
                self.stdout.write(self.style.SUCCESS(f'Usuario "{username}" creado con contraseña "password123"'))
            else:
                # Si el usuario ya existe, asegurarse de que tenga perfil
                if not hasattr(user, 'perfilusuario'):
                    PerfilUsuario.objects.create(usuario=user, rol=rol)
                    self.stdout.write(self.style.SUCCESS(f'Perfil "{rol}" creado para usuario "{username}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Usuario "{username}" ya existe con perfil'))

        self.stdout.write(self.style.SUCCESS('Configuración inicial completada'))
