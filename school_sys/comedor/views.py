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
from pagos.models import Adeudo
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
            
            return Response({
                "message": "Asistencia registrada y adeudo generado.",
                "asistencia_id": asistencia.id,
                "costo": asistencia.precio_aplicado
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

@api_view(['GET', 'POST'])
@permission_classes([CanManageComedor])
def admin_menu_semanal(request):
    """
    GET: Obtener menú semanal de la semana actual (o por fecha)
    POST: Crear/Actualizar menú semanal
    """
    if request.method == 'GET':
        hoy = timezone.now().date()
        fecha_target = request.query_params.get('fecha')
        
        if fecha_target:
            # Si dan fecha, buscar la semana que contiene esa fecha
            try:
                # Lógica simple: Buscar si existe un MenuSemanal que inicie cerca
                # Idealmente MenuSemanal tiene fecha_inicio y cubre 7 dias
                menu_semanal = MenuSemanal.objects.filter(semana_inicio__lte=fecha_target).order_by('-semana_inicio').first()
            except:
                menu_semanal = None
        else:
            # Buscar el más reciente o el de esta semana
            inicio_semana = hoy - timezone.timedelta(days=hoy.weekday())
            menu_semanal = MenuSemanal.objects.filter(semana_inicio=inicio_semana).first()
            
            if not menu_semanal:
                # Fallback al último creado
                menu_semanal = MenuSemanal.objects.order_by('-semana_inicio').first()

        if not menu_semanal:
            return Response({"detail": "No hay menú semanal configurado"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = MenuSemanalSerializer(menu_semanal)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuSemanalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estudiante_menu_actual(request):
    """Retorna el menú semanal activo."""
    hoy = timezone.now().date()
    menu_semanal = MenuSemanal.objects.filter(
        semana_inicio__lte=hoy, 
        semana_fin__gte=hoy, 
        activo=True
    ).first()
    
    if not menu_semanal:
        menu_semanal = MenuSemanal.objects.filter(activo=True).order_by('-semana_inicio').first()

    if not menu_semanal:
        return Response({"detail": "No hay menú disponible", "data": []}, status=200)
        
    serializer = MenuSemanalSerializer(menu_semanal)
    return Response(serializer.data)
