import os
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from users.models import User
from estudiantes.models import NivelEducativo, Grado, CicloEscolar, Grupo, Estudiante
from academico.models import (
    ProgramaEducativo, Materia, PeriodoEvaluacion, Maestro, 
    AdministradorEscolar, AsignacionMaestro, Calificacion, 
    CalificacionFinal, AutorizacionCambioCalificacion
)

def run():
    print("--- INICIANDO VERIFICACIÓN DE FLUJO ACADÉMICO ---")

    # 1. Crear Nivel Educativo y Ciclo (Prerrequisitos)
    nivel, _ = NivelEducativo.objects.get_or_create(nombre="PRIMARIA_TEST", orden=10, grados_totales=6)
    ciclo, _ = CicloEscolar.objects.get_or_create(
        nombre="2025-2026-TEST", 
        defaults={'fecha_inicio': date(2025, 9, 1), 'fecha_fin': date(2026, 7, 15), 'activo': True}
    )
    grado, _ = Grado.objects.get_or_create(nombre="1A_TEST", nivel_educativo=nivel, numero_grado=1)
    
    # 2. Programa Educativo
    programa, created = ProgramaEducativo.objects.get_or_create(
        nivel_educativo=nivel,
        defaults={
            'nombre': "Programa Primaria 2025 TEST",
            'fecha_inicio': date(2025, 9, 1),
            'numero_periodos_evaluacion': 3,
            'activo': True
        }
    )
    print(f"Programa creado: {programa.nombre}")

    # 3. Materia
    materia, _ = Materia.objects.get_or_create(
        clave="MAT-1P-TEST",
        defaults={
            'grado': grado,
            'programa_educativo': programa,
            'nombre': "Matemáticas I",
            'fecha_inicio': date(2025, 9, 1),
            'orden': 1
        }
    )
    print(f"Materia creada: {materia.nombre}")

    # 4. Periodo Evaluacion (Simular ventana activa)
    today = date.today()
    periodo, _ = PeriodoEvaluacion.objects.get_or_create(
        ciclo_escolar=ciclo,
        programa_educativo=programa,
        numero_periodo=1,
        defaults={
            'nombre': "Parcial 1",
            'fecha_inicio': today - timedelta(days=30),
            'fecha_fin': today + timedelta(days=2), # Termina en 2 días, ventana abierta
            'estatus': 'ACTIVO'
        }
    )
    # Forzar fechas para test
    periodo.fecha_fin = today + timedelta(days=2)
    periodo.save() # Recalcula ventanas
    print(f"Periodo creado: {periodo.nombre}, Captura inicia: {periodo.fecha_inicio_captura}, termina: {periodo.fecha_fin_captura}")

    import random
    suffix = random.randint(1000, 9999)
    
    user_maestro, _ = User.objects.get_or_create(
        email=f"maestro_test_{suffix}@school.com", 
        defaults={'role': 'maestro', 'username': f'maestro_test_{suffix}'}
    )
    maestro, _ = Maestro.objects.get_or_create(
        usuario=user_maestro,
        defaults={
            'nivel_educativo': nivel,
            'nombre': "Profesor", 'apellido_paterno': "X", 'apellido_materno': "Y",
            'fecha_contratacion': date.today(),
            'email': f"maestro_test_{suffix}@school.com"
        }
    )

    user_admin, _ = User.objects.get_or_create(
        email=f"admin_escolar_test_{suffix}@school.com", 
        defaults={'role': 'admin_escolar', 'username': f'admin_test_{suffix}'}
    )
    admin_escolar, _ = AdministradorEscolar.objects.get_or_create(
        usuario=user_admin,
        defaults={
            'nivel_educativo': nivel,
            'nombre': "Director", 'apellido_paterno': "Z", 'apellido_materno': "W",
            'email': f"admin_escolar_test_{suffix}@school.com"
        }
    )

    # 6. Grupo y Asignación
    grupo, _ = Grupo.objects.get_or_create(nombre="A_TEST", grado=grado, ciclo_escolar=ciclo)
    asignacion, _ = AsignacionMaestro.objects.get_or_create(
        grupo=grupo, materia=materia, ciclo_escolar=ciclo,
        defaults={'maestro': maestro}
    )
    print(f"Asignación creada: {asignacion}")

    # 7. Estudiante
    user_est, _ = User.objects.get_or_create(
        email=f"estudiante_test_{suffix}@school.com", 
        defaults={'role': 'estudiante', 'username': f'est_test_{suffix}'}
    )
    
    # Check if estudiante exists first to avoid pk issues if we don't know the matricula
    if not hasattr(user_est, 'perfil_estudiante'):
         estudiante = Estudiante.objects.create(
            usuario=user_est,
            nombre="Juanito", apellido_paterno="Perez", apellido_materno="Lopez",
            direccion="Calle Falsa 123"
         )
    else:
         estudiante = user_est.perfil_estudiante

    # 8. Captura Calificación
    print("Intentando capturar calificación...")
    try:
        calif = Calificacion.objects.create(
            estudiante=estudiante,
            asignacion_maestro=asignacion,
            periodo_evaluacion=periodo,
            calificacion=Decimal('9.5'),
            capturada_por=maestro
        )
        print(f"Calificación capturada: {calif.calificacion}, Puede modificar: {calif.puede_modificar}")
    except Exception as e:
        print(f"Error al capturar: {e}")
        calif = Calificacion.objects.get(estudiante=estudiante, asignacion_maestro=asignacion, periodo_evaluacion=periodo)


    # 9. Verificar bloqueo
    if not calif.puede_modificar:
        print("VERIFICADO: Calificación bloqueada automáticamente.")

    # 10. Autorización cambio
    print("Creando autorización de cambio...")
    auth = AutorizacionCambioCalificacion.objects.create(
        calificacion=calif,
        autorizado_por=admin_escolar,
        motivo="Error de dedo"
    )
    
    # Simular uso de auth
    calif.puede_modificar = True
    calif.save()
    print(f"Desbloqueada: {calif.puede_modificar}")
    
    calif.calificacion = Decimal('10.0')
    calif.modificada_por = maestro
    calif.save()
    
    auth.utilizada = True
    auth.valor_anterior = Decimal('9.5')
    auth.valor_nuevo = Decimal('10.0')
    auth.save()
    
    print(f"Modificada a: {calif.calificacion}, Bloqueada de nuevo: {not calif.puede_modificar}")

    # 11. Calificación Final (Simulación)
    print("Calculando final (simulado)...")
    CalificacionFinal.objects.update_or_create(
        estudiante=estudiante, materia=materia, ciclo_escolar=ciclo,
        defaults={
            'calificaciones_periodos': {"P1": 10.0},
            'calificacion_final': 10.0,
            'estatus': 'AO'
        }
    )
    print("Calificación final guardada.")

    print("--- TODO OK ---")

if __name__ == '__main__':
    run()
