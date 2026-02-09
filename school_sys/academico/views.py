from rest_framework import status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    Maestro, Grupo, Materia, AsignacionMaestro, PeriodoEvaluacion,
    Calificacion, AutorizacionCambioCalificacion
)
from estudiantes.models import Estudiante, CicloEscolar
from .serializers import (
    MaestroSerializer, GrupoSerializer, MateriaSerializer,
    AsignacionMaestroSerializer, PeriodoEvaluacionSerializer,
    CalificacionSerializer, EstudianteSimpleSerializer
)
from .permissions import (
    IsAdministradorEscolar, IsMaestro, IsEstudiante
    # Nota: Los object permissions IsAdminEscolarDelMismoNivel y IsMaestroDelMismoNivel 
    # se aplicarán manualmente dentro de las funciones ya que son FBV.
)

# Helper para paginación
def paginate_queryset(queryset, request, serializer_class, context=None):
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serializer = serializer_class(page, many=True, context=context)
        return paginator.get_paginated_response(serializer.data)
    serializer = serializer_class(queryset, many=True, context=context)
    return Response(serializer.data)

# =============================================================================
# VISTAS: ADMINISTRADOR ESCOLAR
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_maestros_list(request):
    """Listar maestros del mismo nivel educativo del administrador."""
    admin = request.user.admin_escolar_perfil
    queryset = Maestro.objects.filter(
        nivel_educativo=admin.nivel_educativo
    ).annotate(
        num_asignaciones=Count('asignaciones', filter=Q(asignaciones__activa=True))
    ).select_related('nivel_educativo', 'usuario')
    
    # Búsqueda
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(
            Q(nombre__icontains=search) | 
            Q(apellido_paterno__icontains=search) | 
            Q(email__icontains=search)
        )
    
    return paginate_queryset(queryset, request, MaestroSerializer)

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_grupos_list(request):
    """Listar grupos del nivel del administrador."""
    admin = request.user.admin_escolar_perfil
    queryset = Grupo.objects.filter(
        grado__nivel_educativo=admin.nivel_educativo
    ).annotate(
        num_estudiantes=Count('inscripciones', filter=Q(inscripciones__estatus='activo')), 
        num_materias=Count('asignaciones_maestro', filter=Q(asignaciones_maestro__activa=True))
    ).select_related('grado', 'ciclo_escolar').order_by('-ciclo_escolar__fecha_inicio', 'grado__orden_global', 'nombre')
    
    return paginate_queryset(queryset, request, GrupoSerializer)

@api_view(['GET', 'POST'])
@permission_classes([IsAdministradorEscolar])
def admin_materias_list_create(request):
    """Listar y crear materias en el nivel del administrador."""
    admin = request.user.admin_escolar_perfil
    
    if request.method == 'GET':
        queryset = Materia.objects.filter(
            grado__nivel_educativo=admin.nivel_educativo
        ).annotate(
            num_asignaciones=Count('asignaciones', filter=Q(asignaciones__activa=True))
        ).select_related('grado', 'programa_educativo')
        
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(nombre__icontains=search) | Q(clave__icontains=search))
            
        return paginate_queryset(queryset, request, MateriaSerializer)
    
    elif request.method == 'POST':
        serializer = MateriaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdministradorEscolar])
def admin_materia_desactivar(request, pk):
    """Desactivar una materia (cambio lógico)."""
    admin = request.user.admin_escolar_perfil
    materia = get_object_or_404(Materia, pk=pk)
    
    # Validación de nivel
    if materia.grado.nivel_educativo != admin.nivel_educativo:
        return Response({"status": "error", "message": "No tiene permiso sobre esta materia"}, status=403)
        
    if materia.asignaciones.filter(activa=True).exists():
         return Response(
             {"status": "error", "message": "No se puede desactivar materia con asignaciones activas"},
             status=status.HTTP_400_BAD_REQUEST
         )
    materia.activa = False
    materia.fecha_fin = timezone.now().date()
    materia.save()
    return Response({"status": "success", "message": "Materia desactivada"})

@api_view(['GET', 'POST'])
@permission_classes([IsAdministradorEscolar])
def admin_asignaciones_list_create(request):
    """Listar y crear asignaciones de maestros."""
    admin = request.user.admin_escolar_perfil
    
    if request.method == 'GET':
        queryset = AsignacionMaestro.objects.filter(
            grupo__grado__nivel_educativo=admin.nivel_educativo
        ).select_related(
            'maestro', 'grupo', 'materia', 'ciclo_escolar'
        ).annotate(
            num_calificaciones=Count('calificaciones')
        )
        return paginate_queryset(queryset, request, AsignacionMaestroSerializer)
    
    elif request.method == 'POST':
        serializer = AsignacionMaestroSerializer(data=request.data)
        if serializer.is_valid():
            # Validar que los objetos pertenecen al nivel del admin
            grupo = serializer.validated_data['grupo']
            if grupo.grado.nivel_educativo != admin.nivel_educativo:
                return Response({"status": "error", "message": "El grupo no pertenece a su nivel"}, status=403)
            
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_materias_disponibles(request):
    """Lista materias disponibles para un grupo (sin maestro asignado)."""
    grupo_id = request.query_params.get('grupo_id')
    if not grupo_id:
         return Response({"status": "error", "message": "grupo_id requerido"}, status=400)
    
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    admin = request.user.admin_escolar_perfil
    if grupo.grado.nivel_educativo != admin.nivel_educativo:
         return Response({"status": "error", "message": "No tiene acceso a este grupo"}, status=403)

    asignadas_ids = AsignacionMaestro.objects.filter(
         grupo=grupo, activa=True
    ).values_list('materia_id', flat=True)

    materias = Materia.objects.filter(
         grado=grupo.grado, activa=True
    ).exclude(id__in=asignadas_ids)

    data = [{
         "materia_id": m.id,
         "nombre": m.nombre,
         "clave": m.clave,
         "display": f"{grupo.nombre} - {m.nombre}"
    } for m in materias]
    
    return Response({"status": "success", "data": data})

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_calificaciones_list(request):
    """Listar todas las calificaciones registradas en el nivel."""
    admin = request.user.admin_escolar_perfil
    queryset = Calificacion.objects.filter(
        estudiante__inscripciones__grupo__grado__nivel_educativo=admin.nivel_educativo
    ).distinct().select_related('estudiante', 'asignacion_maestro__materia', 'periodo_evaluacion')
    
    return paginate_queryset(queryset, request, CalificacionSerializer)

@api_view(['POST'])
@permission_classes([IsAdministradorEscolar])
def admin_calificacion_autorizar(request, pk):
    """Autorizar cambio de una calificación bloqueada."""
    admin = request.user.admin_escolar_perfil
    calificacion = get_object_or_404(Calificacion, pk=pk)
    
    # Validar nivel
    if calificacion.estudiante.inscripciones.filter(grupo__grado__nivel_educativo=admin.nivel_educativo).exists() == False:
         return Response({"status": "error", "message": "Sin permiso sobre este estudiante"}, status=403)

    motivo = request.data.get('motivo', 'Autorizado por administrador')
    calificacion.puede_modificar = True
    calificacion.autorizada_por = admin
    calificacion.save()
    
    AutorizacionCambioCalificacion.objects.create(
        calificacion=calificacion,
        autorizado_por=admin,
        motivo=motivo,
        valor_anterior=calificacion.calificacion
    )
    
    return Response({"status": "success", "message": "Cambio autorizado para el maestro"})

@api_view(['GET', 'POST'])
@permission_classes([IsAdministradorEscolar])
def admin_periodos_list_create(request):
    """Listar y gestionar periodos de evaluación."""
    admin = request.user.admin_escolar_perfil
    
    if request.method == 'GET':
        queryset = PeriodoEvaluacion.objects.filter(
            programa_educativo__nivel_educativo=admin.nivel_educativo
        )
        return paginate_queryset(queryset, request, PeriodoEvaluacionSerializer)
    
    elif request.method == 'POST':
        serializer = PeriodoEvaluacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# VISTAS: MAESTRO
# =============================================================================

@api_view(['GET'])
@permission_classes([IsMaestro])
def maestro_asignaciones_list(request):
    """Listar materias asignadas al maestro en el ciclo activo."""
    maestro = request.user.maestro_perfil
    queryset = AsignacionMaestro.objects.filter(
        maestro=maestro, activa=True, ciclo_escolar__activo=True
    )
    return paginate_queryset(queryset, request, AsignacionMaestroSerializer)

@api_view(['GET'])
@permission_classes([IsMaestro])
def maestro_estudiantes_list(request):
    """Listar estudiantes de los grupos del maestro."""
    maestro = request.user.maestro_perfil
    grupos_ids = AsignacionMaestro.objects.filter(
        maestro=maestro, activa=True, ciclo_escolar__activo=True
    ).values_list('grupo_id', flat=True)
    
    queryset = Estudiante.objects.filter(
        inscripciones__grupo_id__in=grupos_ids,
        inscripciones__estatus='activo'
    ).distinct()
    
    return paginate_queryset(queryset, request, EstudianteSimpleSerializer)

@api_view(['GET', 'POST'])
@permission_classes([IsMaestro])
def maestro_calificaciones_list_create(request):
    """Listar sus capturas o crear una nueva calificación."""
    maestro = request.user.maestro_perfil
    
    if request.method == 'GET':
        queryset = Calificacion.objects.filter(
            asignacion_maestro__maestro=maestro
        ).select_related('estudiante', 'asignacion_maestro__materia', 'periodo_evaluacion')
        return paginate_queryset(queryset, request, CalificacionSerializer)
        
    elif request.method == 'POST':
        # Validar ventana de captura
        periodo_id = request.data.get('periodo_evaluacion')
        periodo = get_object_or_404(PeriodoEvaluacion, pk=periodo_id)
        today = timezone.now().date()
        
        if not (periodo.fecha_inicio_captura <= today <= periodo.fecha_fin_captura):
             return Response(
                 {"status": "error", "message": "Fuera de ventana de captura"},
                 status=status.HTTP_400_BAD_REQUEST
             )
        
        # Validar asignación
        asignacion_id = request.data.get('asignacion_maestro')
        asignacion = get_object_or_404(AsignacionMaestro, pk=asignacion_id)
        if asignacion.maestro != maestro:
             return Response({"status": "error", "message": "Asignacion incorrecta"}, status=403)

        serializer = CalificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(capturada_por=maestro)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsMaestro])
def maestro_solicitar_cambio(request, pk):
    """Solicitar autorización para cambiar una calificación bloqueada."""
    maestro = request.user.maestro_perfil
    calificacion = get_object_or_404(Calificacion, pk=pk)
    
    if calificacion.asignacion_maestro.maestro != maestro:
        return Response({"status": "error", "message": "No tiene permiso sobre esta calificación"}, status=403)
        
    # Aquí iría lógica de notificación real
    return Response({"status": "success", "message": "Solicitud enviada al administrador"})

# =============================================================================
# VISTAS: ESTUDIANTE
# =============================================================================

@api_view(['GET'])
@permission_classes([IsEstudiante])
def estudiante_historial_view(request):
    """Consultar historial académico del estudiante autenticado."""
    estudiante = request.user.perfil_estudiante
    queryset = Calificacion.objects.filter(
        estudiante=estudiante
    ).select_related('asignacion_maestro__materia', 'periodo_evaluacion', 'asignacion_maestro__maestro')
    
    return paginate_queryset(queryset, request, CalificacionSerializer)
