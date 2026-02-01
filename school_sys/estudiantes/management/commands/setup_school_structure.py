from django.core.management.base import BaseCommand
from estudiantes.models import NivelEducativo, Grado, CicloEscolar
from django.utils import timezone
import datetime
from estudiantes.services import asegurar_grupos_ciclo

class Command(BaseCommand):
    help = 'Crea la estructura inicial de niveles educativos, grados y ciclo escolar'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando configuración de estructura escolar...'))

        # 1. Crear Niveles Educativos
        niveles_data = [
            {'nombre': 'Preescolar', 'orden': 1, 'grados_totales': 3},
            {'nombre': 'Primaria', 'orden': 2, 'grados_totales': 6},
            {'nombre': 'Secundaria', 'orden': 3, 'grados_totales': 3},
        ]

        niveles_objs = {}
        for data in niveles_data:
            nivel, created = NivelEducativo.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'orden': data['orden'],
                    'grados_totales': data['grados_totales']
                }
            )
            niveles_objs[data['nombre']] = nivel
            if created:
                self.stdout.write(self.style.SUCCESS(f'Creado nivel: {nivel.nombre}'))
            else:
                self.stdout.write(f'Existente nivel: {nivel.nombre}')

        # 2. Crear Grados
        # Preescolar 1-3
        orden_global = 1
        for i in range(1, 4):
            nombre_grado = f"{i}°"
            grado, created = Grado.objects.get_or_create(
                nombre=nombre_grado,
                nivel=niveles_objs['Preescolar'].nombre, # Mantenemos compatibilidad string
                defaults={
                    'nivel_educativo': niveles_objs['Preescolar'],
                    'numero_grado': i,
                    'orden_global': orden_global
                }
            )
            if not created:
                grado.nivel_educativo = niveles_objs['Preescolar']
                grado.orden_global = orden_global
                grado.numero_grado = i
                grado.save()
            orden_global += 1
            self.stdout.write(f'Procesado grado: {grado}')

        # Primaria 1-6
        for i in range(1, 7):
            nombre_grado = f"{i}°"
            grado, created = Grado.objects.get_or_create(
                nombre=nombre_grado,
                nivel=niveles_objs['Primaria'].nombre,
                defaults={
                    'nivel_educativo': niveles_objs['Primaria'],
                    'numero_grado': i,
                    'orden_global': orden_global
                }
            )
            if not created:
                grado.nivel_educativo = niveles_objs['Primaria']
                grado.orden_global = orden_global
                grado.numero_grado = i
                grado.save()
            orden_global += 1
            self.stdout.write(f'Procesado grado: {grado}')

        # Secundaria 1-3
        for i in range(1, 4):
            nombre_grado = f"{i}°"
            grado, created = Grado.objects.get_or_create(
                nombre=nombre_grado,
                nivel=niveles_objs['Secundaria'].nombre,
                defaults={
                    'nivel_educativo': niveles_objs['Secundaria'],
                    'numero_grado': i,
                    'orden_global': orden_global
                }
            )
            if not created:
                grado.nivel_educativo = niveles_objs['Secundaria']
                grado.orden_global = orden_global
                grado.numero_grado = i
                grado.save()
            orden_global += 1
            self.stdout.write(f'Procesado grado: {grado}')

        # 3. Identificar Ciclo Escolar Activo
        ciclo = CicloEscolar.objects.filter(activo=True).first()
        
        if not ciclo:
            # Si no hay ninguno activo, crear/usar el default
            ciclo_nombre = "2024-2025"
            inicio = datetime.date(2024, 8, 20)
            fin = datetime.date(2025, 7, 15)
            
            ciclo, created = CicloEscolar.objects.get_or_create(
                nombre=ciclo_nombre,
                defaults={
                    'fecha_inicio': inicio,
                    'fecha_fin': fin,
                    'activo': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Creado ciclo escolar default: {ciclo}'))
            else:
                ciclo.activo = True
                ciclo.save()
                self.stdout.write(f'Activado ciclo escolar existente: {ciclo}')
        else:
            self.stdout.write(self.style.SUCCESS(f'Usando ciclo escolar activo: {ciclo}'))

        # 4. Crear Grupos (A, B, C) para cada Grado en el ciclo identificado
        self.stdout.write(self.style.WARNING(f'Asegurando grupos A, B y C para el ciclo {ciclo.nombre}...'))
        
        grupos_count = asegurar_grupos_ciclo(ciclo)

        self.stdout.write(self.style.SUCCESS(f'Se crearon {grupos_count} grupos nuevos para el ciclo {ciclo.nombre}.'))
        self.stdout.write(self.style.SUCCESS('Estructura escolar configurada exitosamente.'))



