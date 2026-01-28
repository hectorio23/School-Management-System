from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from django.db.models import Q
from .models import CicloEscolar, Inscripcion, Estudiante, Grupo, Grado, BecaEstudiante
from pagos.models import Adeudo, ConceptoPago, Pago
from .models import NivelEducativo

def calcular_siguiente_grado(inscripcion_actual):
    """Calcula el siguiente grado o nivel educativo"""
    if not inscripcion_actual or not inscripcion_actual.get_grupo() or not inscripcion_actual.get_grado():
        return None
        
    grado_actual = inscripcion_actual.get_grado()
    nivel_actual = grado_actual.nivel_educativo
    
    if not nivel_actual:
        return None

    # Caso 1: Último grado del nivel
    if grado_actual.numero_grado >= nivel_actual.grados_totales:
        if nivel_actual.nombre == "Secundaria" or nivel_actual.orden == 3:
            return "EGRESADO"
        else:
            siguiente_orden = nivel_actual.orden + 1
            try:

                siguiente_nivel = NivelEducativo.objects.get(orden=siguiente_orden)
                return Grado.objects.get(nivel_educativo=siguiente_nivel, numero_grado=1)
            except Exception:
                return None

    # Caso 2: Siguiente grado mismo nivel
    else:
        try:
            return Grado.objects.get(nivel_educativo=nivel_actual, numero_grado=grado_actual.numero_grado + 1)
        except Grado.DoesNotExist:
            return None

def generar_adeudos_reinscripcion(ciclo_anterior):
    """Genera adeudos de reinscripcion para alumnos activos"""
    inscripciones_activas = Inscripcion.objects.filter(
        ciclo_escolar=ciclo_anterior,
        estatus='activo'
    ).select_related('grupo__grado__nivel_educativo', 'estudiante')
    
    PRECIOS = {'Preescolar': 1000.0, 'Primaria': 1500.0, 'Secundaria': 2000.0, 'Default': 1500.0}
    
    resultados = {"procesados": 0, "egresados": 0, "adeudos_creados": 0, "errores": []}
    
    for insc in inscripciones_activas:
        resultados["procesados"] += 1
        destino = calcular_siguiente_grado(insc)
        
        if destino == "EGRESADO":
            insc.estatus = 'egresado'
            insc.save()
            resultados["egresados"] += 1
            continue
            
        if not destino:
            resultados["errores"].append(f"No destino: {insc.estudiante}")
            continue
            
        nivel = destino.nivel_educativo
        monto = PRECIOS.get(nivel.nombre, PRECIOS['Default'])
        
        concepto, _ = ConceptoPago.objects.get_or_create(
            nombre=f"Reinscripción {nivel.nombre} Automática",
            tipo_concepto='reinscripcion',
            nivel_educativo=nivel.nombre,
            defaults={'monto_base': monto, 'activo': True}
        )
             
        hoy = timezone.now().date()
        if not Adeudo.objects.filter(estudiante=insc.estudiante, concepto=concepto, fecha_generacion__year=hoy.year).exists():
            Adeudo.objects.create(
                estudiante=insc.estudiante,
                concepto=concepto,
                monto_base=concepto.monto_base,
                fecha_generacion=hoy,
                estatus='pendiente',
                generado_automaticamente=True
            )
            insc.estatus = 'pendiente_pago'
            insc.save()
            resultados["adeudos_creados"] += 1
            
    return resultados

def asegurar_grupos_ciclo(ciclo):
    """Crea grupos A, B, C para todos los grados en un ciclo"""
    grados = Grado.objects.all()
    count = 0
    for g in grados:
        for n in ['A', 'B', 'C']:
            _, created = Grupo.objects.get_or_create(
                nombre=n, grado=g, ciclo_escolar=ciclo,
                defaults={'capacidad_maxima': 30}
            )
            if created: count += 1
    return count

def procesar_reinscripcion_automatica(obj):
    """Ejecuta reinscripcion al pagar adeudo de tipo 'reinscripcion'"""
    adeudo = obj.adeudo if isinstance(obj, Pago) else obj
    if not adeudo or adeudo.concepto.tipo_concepto != 'reinscripcion' or adeudo.estatus != 'pagado':
        return False
        
    est = adeudo.estudiante
    last = Inscripcion.objects.filter(estudiante=est, estatus__in=['activo', 'pendiente_pago', 'completado']).order_by('-fecha_inscripcion').first()
    
    if not last: return False
    dest = calcular_siguiente_grado(last)
    if not dest or dest == "EGRESADO": return False
    
    ciclo_n = CicloEscolar.objects.filter(activo=True).first()
    if not ciclo_n or ciclo_n == last.ciclo_escolar: return False
    
    # Buscar grupo destino
    letra = last.grupo.nombre
    g_dest = Grupo.objects.filter(grado=dest, ciclo_escolar=ciclo_n, nombre=letra).first() or \
             Grupo.objects.filter(grado=dest, ciclo_escolar=ciclo_n).first()

    if not g_dest:
        g_dest = Grupo.objects.create(nombre=letra or "A", grado=dest, ciclo_escolar=ciclo_n)
        
    nueva, created = Inscripcion.objects.get_or_create(
        estudiante=est, ciclo_escolar=ciclo_n,
        defaults={'grupo': g_dest, 'estatus': 'activo'}
    )
    
    if not created:
        nueva.estatus = 'activo'
        nueva.grupo = g_dest
        nueva.save()

    if last.estatus != 'completado':
        last.estatus = 'completado'
        last.save()
        
    return True
