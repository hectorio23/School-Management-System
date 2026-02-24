#!/usr/bin/env python
"""
Cronjob: Generación de adeudos de reinscripción
==============================================

Ejecutar: python manage.py shell < cron_reinscripcion.py
Alternativa: python manage.py runscript cron_reinscripcion (si se usa django-extensions)

Frecuencia recomendada: Una vez al crear ciclo escolar (manual o automático)
Cron: 0 0 1 8 * (1 de agosto a medianoche, inicio de ciclo típico)

Comportamiento:
1. Obtiene el ciclo escolar activo más reciente
2. Genera adeudo "Reinscripción [nombre ciclo]" para cada estudiante activo
3. Cambia el status de los estudiantes a "No Reinscrito"
4. Excluye estudiantes con status: Baja, Egresado, No Reinscrito

Variables de entorno requeridas:
- Ninguna adicional (usa configuración de Django)
"""

import os
import sys
import django

# Configurar Django si no está configurado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from django.utils import timezone
from django.db import transaction
from decimal import Decimal

from estudiantes.models import Estudiante, EstadoEstudiante, HistorialEstadosEstudiante, CicloEscolar
from pagos.models import ConceptoPago, Adeudo


def generar_adeudos_reinscripcion():
    """
    Genera adeudos de reinscripción para todos los estudiantes activos
    y cambia su status a 'No Reinscrito'.
    """
    print("[CRON] Iniciando generación de adeudos de reinscripción...")
    
    # 1. Obtener ciclo escolar activo
    ciclo_activo = CicloEscolar.objects.filter(activo=True).first()
    if not ciclo_activo:
        print("[ERROR] No hay ciclo escolar activo. Abortando.")
        return
    
    print(f"[INFO] Ciclo activo: {ciclo_activo.nombre}")
    
    # 2. Obtener estado "Activo" y "No Reinscrito"
    estado_activo = EstadoEstudiante.objects.filter(
        nombre__iexact='Activo',
        es_estado_activo=True
    ).first()
    
    if not estado_activo:
        print("[ERROR] No existe el estado 'Activo'. Abortando.")
        return
    
    estado_no_reinscrito, created = EstadoEstudiante.objects.get_or_create(
        nombre='No Reinscrito',
        defaults={
            'descripcion': 'Pendiente de pago de reinscripción',
            'es_estado_activo': False
        }
    )
    
    if created:
        print("[INFO] Creado estado 'No Reinscrito'")
    
    # 3. Obtener o crear concepto de reinscripción
    nombre_concepto = f"Reinscripción {ciclo_activo.nombre}"
    concepto, created = ConceptoPago.objects.get_or_create(
        nombre=nombre_concepto,
        defaults={
            'descripcion': f'Pago de reinscripción para el ciclo {ciclo_activo.nombre}',
            'monto_base': Decimal('1500.00'),  # Monto base por defecto
            'nivel_educativo': 'Todos',
            'tipo_concepto': 'reinscripcion',
            'activo': True
        }
    )
    
    if created:
        print(f"[INFO] Creado concepto de pago: {nombre_concepto}")
    
    # 4. Obtener estudiantes activos
    # Excluir: Baja, Egresado, No Reinscrito
    estudiantes_activos = Estudiante.objects.filter(
        usuario__activo=True
    ).exclude(
        pk__in=HistorialEstadosEstudiante.objects.filter(
            estado__nombre__in=['Baja', 'Egresado', 'No Reinscrito']
        ).values('estudiante_id')
    )
    
    # También verificar último estado
    estudiantes_procesar = []
    for est in estudiantes_activos:
        estado_actual = est.get_estado_actual()
        if estado_actual and estado_actual.es_estado_activo:
            estudiantes_procesar.append(est)
    
    print(f"[INFO] Estudiantes activos a procesar: {len(estudiantes_procesar)}")
    
    # 5. Generar adeudos y cambiar status
    adeudos_creados = 0
    errores = 0
    
    with transaction.atomic():
        for estudiante in estudiantes_procesar:
            try:
                # Verificar si ya tiene adeudo de reinscripción para este ciclo
                adeudo_existente = Adeudo.objects.filter(
                    estudiante=estudiante,
                    concepto=concepto
                ).exists()
                
                if adeudo_existente:
                    print(f"[SKIP] {estudiante.matricula} ya tiene adeudo de reinscripción")
                    continue
                
                # Calcular monto con descuentos
                monto_base = concepto.monto_base
                descuento = estudiante.get_monto_descuento(monto_base)
                monto_total = max(Decimal('0.00'), monto_base - descuento)
                
                # Crear adeudo
                Adeudo.objects.create(
                    estudiante=estudiante,
                    concepto=concepto,
                    monto_base=monto_base,
                    descuento_aplicado=descuento,
                    monto_total=monto_total,
                    fecha_vencimiento=timezone.now().date() + timezone.timedelta(
                        days=int(os.getenv('DAYS_REINSCRIPCION_DEADLINE', '21'))
                    ),
                    estatus='pendiente',
                    generado_automaticamente=True,
                    justificacion_manual=f'Reinscripción Ciclo {ciclo_activo.nombre}'
                )
                
                # Cambiar status a "No Reinscrito"
                HistorialEstadosEstudiante.objects.create(
                    estudiante=estudiante,
                    estado=estado_no_reinscrito,
                    justificacion=f'Generación automática de reinscripción - Ciclo {ciclo_activo.nombre}'
                )
                
                adeudos_creados += 1
                
            except Exception as e:
                print(f"[ERROR] Estudiante {estudiante.matricula}: {str(e)}")
                errores += 1
    
    print(f"\n[RESULTADO]")
    print(f"  - Adeudos creados: {adeudos_creados}")
    print(f"  - Errores: {errores}")
    print(f"  - Total procesados: {len(estudiantes_procesar)}")


if __name__ == '__main__':
    generar_adeudos_reinscripcion()
else:
    # Si se ejecuta desde manage.py shell
    generar_adeudos_reinscripcion()
