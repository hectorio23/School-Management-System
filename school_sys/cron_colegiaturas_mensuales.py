#!/usr/bin/env python
"""
Cronjob: Generación Automática de Colegiaturas Mensuales
========================================================

Ejecutar: python manage.py shell < cron_colegiaturas_mensuales.py

Frecuencia recomendada: Día 1 de cada mes (00:01 AM)
Cron: 1 0 1 * *

Lógica:
1.  Obtener el ciclo escolar activo.
2.  Obtener o crear el ConceptoPago "Colegiatura <Mes> <Año>".
3.  Generar un Adeudo por cada estudiante activo.
4.  Aplicar descuentos por estrato y beca automáticamente.
5.  Fecha de vencimiento: día 10 del mes siguiente.
6.  Evitar duplicados si ya existe un adeudo para ese concepto y estudiante.
"""

import os
import django
from datetime import date
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from django.utils import timezone
from estudiantes.models import (
    Estudiante, CicloEscolar, NivelEducativo,
    HistorialEstadosEstudiante
)
from pagos.models import ConceptoPago, Adeudo

# Nombres de meses en español
MESES_ES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Estados que excluyen al estudiante de generación de adeudos
ESTADOS_EXCLUIDOS = ['Baja', 'Egresado', 'No Reinscrito', 'Suspendido']


def obtener_fecha_vencimiento(anio, mes):
    """Calcula la fecha de vencimiento: día 10 del mes siguiente."""
    if mes == 12:
        return date(anio + 1, 1, 10)
    return date(anio, mes + 1, 10)


def generar_colegiaturas():
    """Genera adeudos de colegiatura para el mes actual."""
    hoy = timezone.localdate()
    mes_actual = hoy.month
    anio_actual = hoy.year
    nombre_mes = MESES_ES[mes_actual]

    print(f"[CRON] Iniciando generación de colegiaturas - {hoy}")
    print(f"[INFO] Mes: {nombre_mes} {anio_actual}")

    # 1. Verificar ciclo escolar activo
    ciclo_activo = CicloEscolar.objects.filter(activo=True).first()
    if not ciclo_activo:
        print("[ERROR] No hay ciclo escolar activo. Abortando.")
        return

    print(f"[INFO] Ciclo activo: {ciclo_activo.nombre}")

    # 2. Fecha de vencimiento
    fecha_vencimiento = obtener_fecha_vencimiento(anio_actual, mes_actual)
    print(f"[INFO] Fecha de vencimiento: {fecha_vencimiento}")

    # 3. Obtener niveles educativos
    niveles = NivelEducativo.objects.all()

    total_generados = 0
    total_duplicados = 0
    total_errores = 0

    for nivel in niveles:
        nombre_concepto = f"Colegiatura {nombre_mes} {anio_actual}"

        # 4. Obtener o crear ConceptoPago para este mes y nivel
        concepto, creado = ConceptoPago.objects.get_or_create(
            nombre=nombre_concepto,
            nivel_educativo=nivel.nombre,
            defaults={
                'descripcion': f'Colegiatura mensual correspondiente a {nombre_mes} {anio_actual}',
                'monto_base': Decimal('0.00'),  # Se tomará del concepto base de colegiatura
                'tipo_concepto': 'colegiatura',
                'activo': True,
            }
        )

        # Si fue creado sin monto, buscar el monto base del concepto de colegiatura genérico
        if creado or concepto.monto_base == Decimal('0.00'):
            concepto_base = ConceptoPago.objects.filter(
                tipo_concepto='colegiatura',
                nivel_educativo=nivel.nombre,
                activo=True
            ).exclude(pk=concepto.pk).first()

            if concepto_base:
                concepto.monto_base = concepto_base.monto_base
                concepto.save()
            else:
                print(f"  [WARN] Sin concepto base de colegiatura para nivel {nivel.nombre}. "
                      f"Se usará monto $0.00")

        if creado:
            print(f"  [NUEVO] Concepto creado: {nombre_concepto} ({nivel.nombre}) - "
                  f"Monto base: ${concepto.monto_base}")
        else:
            print(f"  [INFO] Concepto existente: {nombre_concepto} ({nivel.nombre})")

        # 5. Obtener estudiantes activos de este nivel
        estudiantes = Estudiante.objects.filter(
            usuario__activo=True,
            inscripciones__grupo__grado__nivel_educativo=nivel,
            inscripciones__estatus='activo',
            inscripciones__grupo__ciclo_escolar=ciclo_activo
        ).distinct()

        # Filtrar por estado activo (excluir bajas, egresados, etc.)
        estudiantes_activos = []
        for est in estudiantes:
            estado = est.get_estado_actual()
            if estado and estado.nombre in ESTADOS_EXCLUIDOS:
                continue
            estudiantes_activos.append(est)

        print(f"  [INFO] Estudiantes activos en {nivel.nombre}: {len(estudiantes_activos)}")

        # 6. Generar adeudos
        primer_dia_mes = date(anio_actual, mes_actual, 1)

        for estudiante in estudiantes_activos:
            try:
                # Verificar duplicados
                ya_existe = Adeudo.objects.filter(
                    estudiante=estudiante,
                    concepto=concepto,
                    mes_correspondiente=primer_dia_mes
                ).exists()

                if ya_existe:
                    total_duplicados += 1
                    continue

                # Calcular descuento
                monto_base = concepto.monto_base
                descuento = estudiante.get_monto_descuento(monto_base)
                monto_final = max(Decimal('0.00'), monto_base - descuento)

                # Crear adeudo
                Adeudo.objects.create(
                    estudiante=estudiante,
                    concepto=concepto,
                    monto_base=monto_base,
                    descuento_aplicado=descuento,
                    monto_total=monto_final,
                    fecha_vencimiento=fecha_vencimiento,
                    mes_correspondiente=primer_dia_mes,
                    tipo_adeudo='CONCEPTO DE PAGO',
                    generado_automaticamente=True,
                    estatus='pendiente'
                )
                total_generados += 1

            except Exception as e:
                print(f"  [ERROR] Matrícula {estudiante.matricula}: {e}")
                total_errores += 1

    print(f"\n[RESULTADO]")
    print(f"  - Adeudos generados: {total_generados}")
    print(f"  - Duplicados omitidos: {total_duplicados}")
    print(f"  - Errores: {total_errores}")
    print(f"[CRON] Finalizado.")


if __name__ == '__main__':
    generar_colegiaturas()
else:
    # Si se ejecuta desde manage.py shell
    generar_colegiaturas()
