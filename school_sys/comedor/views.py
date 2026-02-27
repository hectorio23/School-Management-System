import os
from decimal import Decimal
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count, Sum

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.permissions import CanManageComedor
from estudiantes.models import Estudiante
from .models import AsistenciaCafeteria, MenuSemanal, Menu
from pagos.models import Adeudo, Pago
from .serializers import (
    AsistenciaCafeteriaSerializer, 
    MenuSemanalSerializer,
    EstudianteAlergiaSerializer,
    MenuSerializer
)
from users.serializers_admin import AdeudoSerializer

@api_view(['GET'])
@permission_classes([CanManageComedor])
def admin_asistencias_list(request):
    """Lista todas las asistencias registradas (filtro opcional por fecha)."""
    queryset = AsistenciaCafeteria.objects.select_related('estudiante', 'menu').all().order_by('-fecha_asistencia')
    
    fecha = request.query_params.get('fecha')
    if fecha:
        queryset = queryset.filter(fecha_asistencia=fecha)
        
    serializer = AsistenciaCafeteriaSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([CanManageComedor])
def admin_registrar_asistencia(request):
    """
    Registra asistencia y genera adeudo automático.
    Body: { "estudiante_id": <int>, "fecha": "YYYY-MM-DD", "tipo_comida": "Comida/Desayuno" }
    """
    estudiante_id = request.data.get('estudiante_id') or request.data.get('matricula')
    fecha = request.data.get('fecha', timezone.now().date())
    tipo_comida = request.data.get('tipo_comida', 'Comida')
    pagado_fisico = request.data.get('pagado_fisico', False)
    
    
    if not estudiante_id:
        return Response({"error": "Se requiere estudiante_id o matricula"}, status=status.HTTP_400_BAD_REQUEST)

    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    
    # Verificar duplicados
    if AsistenciaCafeteria.objects.filter(estudiante=estudiante, fecha_asistencia=fecha, tipo_comida=tipo_comida).exists():
        return Response({"error": "El estudiante ya tiene asistencia registrada para este día y tipo."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        with transaction.atomic():
            # 1. Registrar Asistencia (El precio se calcula automáticamente en el modelo)
            asistencia = AsistenciaCafeteria.objects.create(
                estudiante=estudiante,
                fecha_asistencia=fecha,
                tipo_comida=tipo_comida
            )
            
            # 2. Generar Adeudo Automático (Manejado en el save() de AsistenciaCafeteria)
            # Ya no creamos AdeudoComedor explícitamente aquí
            
            # 3. Pago Físico Directo
            if pagado_fisico and asistencia.adeudo:
                Pago.objects.create(
                    adeudo=asistencia.adeudo,
                    monto=asistencia.adeudo.monto_total,
                    fecha_pago=timezone.now(),
                    metodo_pago='efectivo',
                    notas='Pago físico directo en cafetería'
                )
                # El guardado del Pago actualizará automáticamente el saldo y estatus del Adeudo

            return Response({
                "message": "Asistencia registrada y adeudo generado.",
                "asistencia_id": asistencia.id,
                "costo": asistencia.precio_aplicado
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageComedor])
def admin_asistencia_detalle(request, pk):
    """
    Gestión de una asistencia específica (Detalle, Actualizar, Eliminar)
    """
    asistencia = get_object_or_404(AsistenciaCafeteria, pk=pk)
    
    if request.method == 'GET':
        serializer = AsistenciaCafeteriaSerializer(asistencia)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        # Permite cambiar tipo de comida o fecha, pero puede requerir re-calcular
        fecha = request.data.get('fecha', asistencia.fecha_asistencia)
        tipo_comida = request.data.get('tipo_comida', asistencia.tipo_comida)
        pagado_fisico = request.data.get('pagado_fisico', False)
        
        # Verificar duplicados si se están cambiando fecha o tipo
        if (fecha != asistencia.fecha_asistencia or tipo_comida != asistencia.tipo_comida) and \
           AsistenciaCafeteria.objects.filter(estudiante=asistencia.estudiante, fecha_asistencia=fecha, tipo_comida=tipo_comida).exclude(pk=pk).exists():
            return Response({"error": "El estudiante ya tiene otra asistencia registrada para este día y tipo."}, status=status.HTTP_400_BAD_REQUEST)
            
        asistencia.fecha_asistencia = fecha
        asistencia.tipo_comida = tipo_comida
        asistencia.save()
        
        # Procesar pago físico si se marcó la casilla y el adeudo no está pagado
        if pagado_fisico and asistencia.adeudo and asistencia.adeudo.estatus != 'pagado':
            Pago.objects.create(
                adeudo=asistencia.adeudo,
                monto=asistencia.adeudo.monto_total,
                fecha_pago=timezone.now(),
                metodo_pago='efectivo',
                notas='Pago físico directo en cafetería (Edición)'
            )
        
        serializer = AsistenciaCafeteriaSerializer(asistencia)
        return Response(serializer.data)
        
    elif request.method == 'DELETE':
        # Si tiene adeudo generado automáticamente, y no está pagado, se puede eliminar.
        # En una regla de negocio más estricta, tal vez haya que revisar si el adeudo tiene pagos parciales.
        if asistencia.adeudo and asistencia.adeudo.monto_pagado == 0:
            asistencia.adeudo.delete()
        asistencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([CanManageComedor])
def admin_reporte_diario(request):
    """Reporte de asistencia del día especificado (o hoy)."""
    fecha = request.query_params.get('fecha', timezone.now().date())
    asistencias = AsistenciaCafeteria.objects.filter(fecha_asistencia=fecha)
    
    total_asistencias = asistencias.count()
    total_recaudado = asistencias.aggregate(Sum('precio_aplicado'))['precio_aplicado__sum'] or 0
    
    return Response({
        "fecha": fecha,
        "total_asistencias": total_asistencias,
        "total_recaudado": total_recaudado,
        "detalles": AsistenciaCafeteriaSerializer(asistencias, many=True).data
    })

@api_view(['GET'])
@permission_classes([CanManageComedor])
def admin_reporte_semanal(request):
    """Reporte semanal. Requiere fecha_inicio y fecha_fin."""
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')
    
    if not fecha_inicio or not fecha_fin:
        # Default: Semana actual
        hoy = timezone.now().date()
        fecha_inicio = hoy - timezone.timedelta(days=hoy.weekday())
        fecha_fin = fecha_inicio + timezone.timedelta(days=6)
        
        # return Response({"error": "Debe proporcionar fecha_inicio y fecha_fin"}, status=status.HTTP_400_BAD_REQUEST)

    asistencias = AsistenciaCafeteria.objects.filter(fecha_asistencia__range=[fecha_inicio, fecha_fin])
    
    por_dia = asistencias.values('fecha_asistencia').annotate(
        total=Count('id'), ingreso=Sum('precio_aplicado')
    ).order_by('fecha_asistencia')
    
    return Response({
        "periodo": f"{fecha_inicio} al {fecha_fin}",
        "total_semana": asistencias.count(),
        "ingreso_semana": asistencias.aggregate(Sum('precio_aplicado'))['precio_aplicado__sum'] or 0,
        "desglose_dia": por_dia
    })

@api_view(['GET'])
@permission_classes([CanManageComedor])
def admin_reporte_mensual(request):
    """Reporte mensual. Requiere mes (1-12) y anio."""
    hoy = timezone.now().date()
    mes = int(request.query_params.get('mes', hoy.month))
    anio = int(request.query_params.get('anio', hoy.year))
    
    asistencias = AsistenciaCafeteria.objects.filter(
        fecha_asistencia__year=anio, 
        fecha_asistencia__month=mes
    )
    
    return Response({
        "mes": mes,
        "anio": anio,
        "total_mes": asistencias.count(),
        "ingreso_mes": asistencias.aggregate(Sum('precio_aplicado'))['precio_aplicado__sum'] or 0,
    })

@api_view(['GET'])
@permission_classes([CanManageComedor])
def admin_alertas_alergias(request):
    """Lista estudiantes con alergias registradas."""
    estudiantes = Estudiante.objects.filter(
        alergias_alimentarias__isnull=False
    ).exclude(alergias_alimentarias="").order_by('apellido_paterno', 'nombre')
    
    serializer = EstudianteAlergiaSerializer(estudiantes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([CanManageComedor])
def admin_historial_asistencia_estudiante(request, matricula):
    """Historial de comedores de un estudiante específico."""
    asistencias = AsistenciaCafeteria.objects.filter(estudiante__matricula=matricula).order_by('-fecha_asistencia')
    adeudos = Adeudo.objects.filter(estudiante__matricula=matricula, tipo_adeudo='COMEDOR').order_by('-fecha_generacion')
    
    return Response({
        "estudiante_id": matricula,
        "total_asistencias": asistencias.count(),
        "adeudos_pendientes": adeudos.exclude(estatus='pagado').count(),
        "historial_asistencia": AsistenciaCafeteriaSerializer(asistencias, many=True).data,
        "adeudos": AdeudoSerializer(adeudos, many=True).data
    })

@api_view(['GET', 'POST'])
@permission_classes([CanManageComedor])
def admin_menus_list(request):
    """
    GET: Listar menús disponibles
    POST: Crear nuevo menú
    """
    if request.method == 'GET':
        menus = Menu.objects.all().order_by('desactivar', 'descripcion')
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageComedor])
def admin_menu_detalle(request, pk):
    """
    Gestión de un menú específico (Detalle, Actualizar, Eliminar)
    """
    menu = get_object_or_404(Menu, pk=pk)
    
    if request.method == 'GET':
        serializer = MenuSerializer(menu)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([CanManageComedor])
def admin_menu_semanal(request):
    """
    GET: Obtener menú semanal de la semana actual (o por fecha)
    POST: Crear/Actualizar menú semanal
    """
    if request.method == 'GET':
        menus = MenuSemanal.objects.all().order_by('-fecha_subida')
        serializer = MenuSemanalSerializer(menus, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        menu_id = request.data.get('id')
        if menu_id:
            try:
                instance = MenuSemanal.objects.get(id=menu_id)
                serializer = MenuSemanalSerializer(instance, data=request.data)
            except MenuSemanal.DoesNotExist:
                return Response({"detail": "Menú no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MenuSemanalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if not menu_id else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estudiante_asistencias(request):
    """Retorna las últimas 10 asistencias del estudiante autenticado."""
    if request.user.role != 'estudiante':
        return Response({"error": "Solo estudiantes pueden acceder a este recurso"}, status=403)
    
    try:
        estudiante = getattr(request.user, 'perfil_estudiante', None)
        if not estudiante:
            estudiante = Estudiante.objects.get(usuario=request.user)
    except Estudiante.DoesNotExist:
        return Response({"error": "Perfil de estudiante no encontrado"}, status=404)
        
    asistencias = AsistenciaCafeteria.objects.filter(estudiante=estudiante).order_by('-fecha_asistencia')[:10]
    serializer = AsistenciaCafeteriaSerializer(asistencias, many=True)
    return Response(serializer.data)

from academico.models import EventoCalendario

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estudiante_menu_actual(request):
    """
    Retorna el menú semanal activo. 
    Considera si hoy es fin de semana o festivo.
    """
    hoy = timezone.now().date()
    
    # 1. Verificar si es fin de semana o día festivo
    es_fin_semana = hoy.weekday() >= 5  # 5=Sábado, 6=Domingo
    es_festivo = EventoCalendario.objects.filter(
        tipo_evento='FESTIVO',
        fecha_inicio__date__lte=hoy,
        fecha_fin__date__gte=hoy
    ).exists()

    if es_fin_semana or es_festivo:
        motivo = "Fin de semana" if es_fin_semana else "Día Festivo"
        return Response({
            "status": "success",
            "is_closed": True,
            "motivo": motivo,
            "menu": None
        })

    # 2. Buscar menú semanal activo (independiente de la fecha)
    menu_semanal = MenuSemanal.objects.filter(activo=True).order_by('-fecha_subida').first()
    
    if not menu_semanal:
        # Fallback al último subido
        menu_semanal = MenuSemanal.objects.order_by('-fecha_subida').first()

    if not menu_semanal:
        return Response({
            "status": "error",
            "detail": "No hay menú disponible para esta semana",
            "menu": None
        })
        
    serializer = MenuSemanalSerializer(menu_semanal)
    
    # El frontend espera que los campos se llamen 'lunes', 'martes', etc.
    # Pero en el modelo son 'lunes_menu', etc.
    # Mapearemos para compatibilidad si es necesario o simplemente devolveremos todo.
    data = serializer.data
    # Crear alias para compatibilidad con el frontend antiguo si es necesario
    for dia in ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']:
        data[dia] = data.get(f"{dia}_menu")

    return Response({
        "status": "success",
        "menu": data
    })
