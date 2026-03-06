import os
import sys
import django
import random
import time
from datetime import datetime, timedelta, date
from decimal import Decimal

# Setup Django
sys.path.append('/home/hectorio23/Desktop/SMS/school_sys')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from django.utils import timezone
from users.models import User
from estudiantes.models import (
    Estudiante, NivelEducativo, Grado, CicloEscolar, Grupo, 
    Estrato, EstadoEstudiante, Inscripcion, Beca
)
from academico.models import (
    ProgramaEducativo, Materia, AsignacionMaestro, Maestro, 
    PeriodoEvaluacion, Calificacion
)
from pagos.models import Adeudo, Pago, ConceptoPago

def simulate_system():
    print("=== INICIANDO SIMULACIÓN DE ESTRÉS / USO COMPLETO ===")
    
    # 1. Asegurar Infraestructura Básica
    print("[1/6] Configurando niveles y grados...")
    niveles_nombres = ['PREESCOLAR', 'PRIMARIA', 'SECUNDARIA']
    niveles = []
    for n in niveles_nombres:
        nivel, _ = NivelEducativo.objects.get_or_create(
            nombre=n, 
            defaults={'orden': niveles_nombres.index(n)+1, 'grados_totales': 6}
        )
        niveles.append(nivel)
        # Crear grados para cada nivel
        for i in range(1, 7):
            Grado.objects.get_or_create(
                nombre=f"{i}°", 
                nivel_educativo=nivel,
                nivel=n,
                defaults={
                    'numero_grado': i,
                    'orden_global': (niveles_nombres.index(n) * 6) + i
                }
            )

    # 2. Ciclo Escolar y Periodos
    print("[2/6] Creando ciclo escolar y programas...")
    ciclo, _ = CicloEscolar.objects.get_or_create(
        nombre=f"CI-2024-2025",
        defaults={
            'fecha_inicio': date(2024, 8, 1),
            'fecha_fin': date(2025, 7, 15),
            'activo': True
        }
    )
    
    # Programa para Primaria
    prog, _ = ProgramaEducativo.objects.get_or_create(
        nombre="Plan de Estudios Primaria 2024",
        defaults={
            'nivel_educativo': niveles[1], # PRIMARIA
            'fecha_inicio': date(2024, 1, 1),
            'numero_periodos_evaluacion': 3,
            'activo': True
        }
    )
    
    # Materias
    materias_nombres = ['Matemáticas', 'Español', 'Ciencias Naturales', 'Historia', 'Geografía', 'Inglés']
    for idx, m_name in enumerate(materias_nombres):
        # Para 1er grado de primaria
        grado1 = Grado.objects.filter(nivel_educativo=niveles[1], numero_grado=1).first()
        Materia.objects.get_or_create(
            clave=f"PRI1-{idx}",
            defaults={
                'grado': grado1,
                'programa_educativo': prog,
                'nombre': m_name,
                'orden': idx
            }
        )

    # 3. Maestros y Estudiantes
    print("[3/6] Simulando maestros y estudiantes (10 de cada uno)...")
    maestros = []
    for i in range(10):
        email = f"maestro{i}@sms.edu"
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': f"maestro{i}", 'role': 'maestro', 'nombre': f"Maestro {i}"}
        )
        if _: user.set_password('pass123'); user.save()
        
        maestro, _ = Maestro.objects.get_or_create(
            usuario=user,
            defaults={
                'nombre': f"Maestro", 'apellido_paterno': f"Simulado {i}",
                'apellido_materno': "Test",
                'nivel_educativo': niveles[1],
                'fecha_contratacion': date(2024, 1, 1)
            }
        )
        maestros.append(maestro)

    # Estudiantes
    estudiantes = []
    for i in range(10):
        email = f"alumno{i}@sms.edu"
        curp = f"CURP{i:05}ALUMNO"
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': curp, 'role': 'estudiante', 'nombre': f"Alumno {i}"}
        )
        if _: user.set_password('pass123'); user.save()
        
        estudiante, _ = Estudiante.objects.get_or_create(
            usuario=user,
            defaults={
                'nombre': f"Alumno", 'apellido_paterno': f"Test {i}",
                'apellido_materno': "Simulado",
                'matricula': f"2024{i:04}"
            }
        )
        estudiantes.append(estudiante)

    # 4. Inscripciones y Asignaciones
    print("[4/6] Inscribiendo alumnos y asignando clases...")
    grupo1A, _ = Grupo.objects.get_or_create(
        nombre="1-A",
        grado=Grado.objects.filter(nivel_educativo=niveles[1], numero_grado=1).first(),
        ciclo_escolar=ciclo,
        defaults={'capacidad_maxima': 30}
    )

    for est in estudiantes:
        Inscripcion.objects.get_or_create(estudiante=est, grupo=grupo1A)

    # Asignaciones Maestro
    materia_math = Materia.objects.get(clave="PRI1-0")
    AsignacionMaestro.objects.get_or_create(
        maestro=maestros[0],
        materia=materia_math,
        grupo=grupo1A,
        ciclo_escolar=ciclo
    )

    # 5. Calificaciones
    print("[5/6] Simulando subida de calificaciones...")
    periodo1, _ = PeriodoEvaluacion.objects.get_or_create(
        ciclo_escolar=ciclo,
        programa_educativo=prog,
        numero_periodo=1,
        defaults={
            'nombre': 'Primer Trimestre',
            'fecha_inicio': date(2024, 8, 1),
            'fecha_fin': date(2024, 11, 30),
            'estatus': 'ACTIVO'
        }
    )
    
    asignacion = AsignacionMaestro.objects.filter(maestro=maestros[0]).first()
    for est in estudiantes:
        Calificacion.objects.update_or_create(
            estudiante=est,
            periodo_evaluacion=periodo1,
            asignacion_maestro=asignacion,
            defaults={
                'calificacion': Decimal(random.randint(6, 10)),
                'capturada_por': maestros[0]
            }
        )

    # 6. Pagos
    print("[6/6] Simulando generación de adeudos y pagos...")
    concepto, _ = ConceptoPago.objects.get_or_create(
        nombre="Mensualidad Septiembre",
        defaults={
            'monto_base': 1500, 
            'nivel_educativo': 'PRIMARIA', 
            'tipo_concepto': 'colegiatura',
            'descripcion': 'Pago de mensualidad de septiembre'
        }
    )

    for est in estudiantes:
        adeudo, created = Adeudo.objects.get_or_create(
            estudiante=est,
            concepto=concepto,
            defaults={'monto_base': 1500, 'monto_total': 1500, 'estatus': 'pendiente'}
        )
        if created or adeudo.estatus == 'pendiente':
            Pago.objects.create(
                adeudo=adeudo,
                monto=adeudo.monto_total,
                metodo_pago='transferencia',
                recibido_por='Simulador'
            )

    print("\n=== SIMULACIÓN COMPLETADA EXITOSAMENTE ===")
    print(f"Total Usuarios: {User.objects.count()}")
    print(f"Total Adeudos: {Adeudo.objects.count()}")
    print(f"Total Calificaciones: {Calificacion.objects.count()}")

if __name__ == "__main__":
    simulate_system()
