"""
Comando para crear los grupos de permisos iniciales del sistema.
Uso: python manage.py crear_grupos_permisos
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Crea los grupos de permisos para administradores del sistema'

    def handle(self, *args, **options):
        grupos = [
            ('gestor_becas', 'Gestión de becas y asignaciones de becas a estudiantes'),
            ('gestor_comedor', 'Gestión del comedor, asistencias y menús'),
            ('gestor_admisiones', 'Gestión del proceso de admisión de aspirantes'),
            ('admin_ti', 'Administrador de TI con acceso total al sistema'),
        ]

        creados = 0
        existentes = 0

        for nombre, descripcion in grupos:
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Grupo "{nombre}" creado')
                )
            else:
                existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'  - Grupo "{nombre}" ya existe')
                )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'Resumen: {creados} grupos creados, {existentes} ya existían')
        )
        self.stdout.write('')
        self.stdout.write('Para asignar grupos a usuarios, usar el panel de Django Admin:')
        self.stdout.write('  1. Ir a /admin/auth/user/<id>/change/')
        self.stdout.write('  2. En la sección "Grupos", seleccionar los grupos deseados')
        self.stdout.write('  3. Guardar cambios')
