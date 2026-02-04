from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404
from django.db import transaction, models
from django.utils import timezone

from .permissions import (
    IsAdministrador, CanAccessStudentInfo, CanManageBecas, 
    CanManageFinanzas, CanManageComedor
)

from .serializers import EmailTokenObtainPairSerializer
from .serializers_admin import (
    TutorSerializer, 
    EstudianteAdminSerializer, 
    EstudianteUpdateSerializer, 
    PagoSerializer, 
    AdeudoSerializer, 
    AdeudoCreateSerializer,
    EvaluacionSerializer,
    ConceptoPagoSerializer,
    GradoSerializer,
    GrupoSerializer,
    EstratoSerializer,
    EstadoEstudianteSerializer,
    BecaSerializer,
    BecaEstudianteSerializer
)
from estudiantes.models import (
    Estudiante, Tutor, EvaluacionSocioeconomica, 
    Grado, Grupo, Estrato, EstadoEstudiante, Beca, BecaEstudiante,
    HistorialEstadosEstudiante, Inscripcion, CicloEscolar
)
from pagos.models import Pago, Adeudo, ConceptoPago

# Imports para Password Reset
import random
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from admissions.models import AdmissionUser, VerificationCode
from users.models import User

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request):
    return render(request, "./dashboard_admin.html")


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class StudentPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 150
    page_size_query_param = 'page_size'
    max_page_size = 1000


# =============================================================================
# ESTUDIANTES
# =============================================================================

@api_view(['GET'])
@permission_classes([CanAccessStudentInfo])
def admin_student_list(request):
    """
    GET /api/admin/students/
    Retorna lista de estudiantes paginada (60 por página).
    Busca la inscripción activa para mostrar grado/grupo.
    """
    paginator = StudentPagination()
    # Usamos prefetch_related para las inscripciones y select_related para optimizar
    students = Estudiante.objects.prefetch_related(
        models.Prefetch(
            'inscripciones',
            queryset=Inscripcion.objects.filter(ciclo_escolar__activo=True).select_related('grupo__grado__nivel_educativo', 'ciclo_escolar'),
            to_attr='active_enrollment'
        )
    ).order_by('matricula')
    
    result_page = paginator.paginate_queryset(students, request)
    
    data = []
    for s in result_page:
        nombre_grado = "S/A"
        nombre_grupo = "S/A"
        
        # Obtener la inscripción activa del atributo prefetched
        active_enroll = s.active_enrollment[0] if s.active_enrollment else None
        
        if active_enroll and active_enroll.grupo:
            nombre_grupo = active_enroll.grupo.nombre
            if active_enroll.grupo.grado:
                grado = active_enroll.grupo.grado
                nivel_nombre = grado.nivel_educativo.nombre if grado.nivel_educativo else grado.nivel
                nombre_grado = f"{grado.nombre} {nivel_nombre}"

        estrato = s.get_estrato_actual()
        estrato_nombre = estrato.nombre if estrato else "Sin Asignar"
        
        estado = s.get_estado_actual()
        estatus_nombre = estado.nombre if estado else "Sin Estado"

        data.append({
            "matricula": s.matricula,
            "apellido_paterno": s.apellido_paterno,
            "apellido_materno": s.apellido_materno,
            "nombres": s.nombre, 
            "grado": nombre_grado,
            "grupo": nombre_grupo,
            "estrato": estrato_nombre,
            "estatus": estatus_nombre,
        })

    return paginator.get_paginated_response(data)


@api_view(['GET'])
@permission_classes([CanAccessStudentInfo])
def admin_student_detail(request, matricula):
    """
    GET /api/admin/students/<matricula>/
    Retorna TODO sobre un alumno: info personal, tutores, historial, deudas, etc.
    """
    try:
        student = Estudiante.objects.select_related('usuario').prefetch_related(
            models.Prefetch(
                'inscripciones',
                queryset=Inscripcion.objects.filter(ciclo_escolar__activo=True).select_related('grupo__grado__nivel_educativo', 'ciclo_escolar'),
                to_attr='active_enrollment'
            )
        ).get(matricula=matricula)
    except Estudiante.DoesNotExist:
        return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    active_enroll = student.active_enrollment[0] if student.active_enrollment else None
    
    # Resolver academic info
    grupo_str = "Sin Grupo"
    grado_str = "Sin Grado"
    ciclo_str = "N/A"
    
    if active_enroll:
        ciclo_str = active_enroll.ciclo_escolar.nombre
        if active_enroll.grupo:
            grupo_str = active_enroll.grupo.nombre
            if active_enroll.grupo.grado:
                grado = active_enroll.grupo.grado
                nivel_nombre = grado.nivel_educativo.nombre if grado.nivel_educativo else grado.nivel
                grado_str = f"{grado.nombre} {nivel_nombre}"

    info_basica = {
        "matricula": student.matricula,
        "nombre_completo": f"{student.nombre} {student.apellido_paterno} {student.apellido_materno}",
        "nombres": student.nombre,
        "apellido_paterno": student.apellido_paterno,
        "apellido_materno": student.apellido_materno,
        "curp": student.usuario.username, 
        "email": student.usuario.email,
        "direccion": student.direccion,
        "grupo": grupo_str,
        "grado": grado_str,
        "ciclo": ciclo_str,
        "porcentaje_beca": student.porcentaje_beca
    }

    tutores_rel = student.estudiantetutor_set.select_related('tutor').all()
    tutores_data = []
    for rel in tutores_rel:
        t = rel.tutor
        tutores_data.append({
            "id": t.id,
            "nombre": f"{t.nombre} {t.apellido_paterno} {t.apellido_materno}",
            "telefono": t.telefono,
            "correo": t.correo,
            "parentesco": rel.parentesco,
            "activo": rel.activo
        })

    historial_estados = student.historialestadosestudiante_set.select_related('estado').order_by('-fecha_creacion')
    estados_data = []
    for h in historial_estados:
        estados_data.append({
            "estado": h.estado.nombre,
            "fecha": h.fecha_creacion,
            "justificacion": h.justificacion
        })

    evaluaciones = student.evaluacionsocioeconomica_set.select_related('estrato').order_by('-fecha_evaluacion')
    evaluaciones_data = []
    for eva in evaluaciones:
        evaluaciones_data.append({
            "fecha": eva.fecha_evaluacion,
            "estrato_resultante": eva.estrato.nombre if eva.estrato else "Pendiente/Nulo",
            "ingreso_mensual": eva.ingreso_mensual,
            "aprobado": eva.aprobado
        })

    estrato_actual = student.get_estrato_actual()
    estado_actual = student.get_estado_actual()
    beca_activa = student.get_beca_activa()
    balance = student.get_balance_total()

    data = {
        "informacion_personal": info_basica,
        "resumen_academico": {
            "ciclo_escolar": ciclo_str,
            "estrato_actual": estrato_actual.nombre if estrato_actual else "N/A",
            "estado_escolar": estado_actual.nombre if estado_actual else "N/A",
            "beca_nombre": beca_activa.nombre if beca_activa else "Ninguna",
            "beca_porcentaje": beca_activa.porcentaje if beca_activa else 0,
            "balance_adeudo": balance
        },
        "tutores": tutores_data,
        "historial_estados": estados_data,
        "evaluaciones_historico": evaluaciones_data,
        "metadata": {
            "usuario_id": student.usuario.id,
            "role": student.usuario.role,
            "activo_sistema": student.usuario.activo
        }
    }

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdministrador])
def admin_student_create(request):
    """
    POST /api/admin/students/create/
    Crear usuario + estudiante transaccionalmente.
    """
    serializer = EstudianteAdminSerializer(data=request.data)
    if serializer.is_valid():
        estudiante = serializer.save()
        return Response(EstudianteAdminSerializer(estudiante).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdministrador])
def admin_student_update(request, matricula):
    """
    PUT /api/admin/students/<matricula>/update/ - Actualizar estudiante
    DELETE /api/admin/students/<matricula>/update/ - Soft delete (baja)
    """
    estudiante = get_object_or_404(Estudiante, matricula=matricula)
    
    if request.method == 'PUT':
        serializer = EstudianteUpdateSerializer(estudiante, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # 1. Obtener estado "Baja"
        try:
            estado_baja = EstadoEstudiante.objects.filter(nombre__iexact='BAJA').first()
            if not estado_baja:
                # Si no existe, intentar con "BAJA DEFINITIVA" como fallback
                estado_baja = EstadoEstudiante.objects.filter(nombre__iexact='BAJA DEFINITIVA').first()
            
            if not estado_baja:
                 return Response({"error": "El estado 'Baja' no existe en el catálogo"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error al buscar estado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Registrar en historial
        HistorialEstadosEstudiante.objects.create(
            estudiante=estudiante,
            estado=estado_baja,
            justificacion="Baja administrativa a través de API Admin",
            fecha_baja=timezone.now().date(),
            es_baja_temporal=False
        )
        
        # 3. Desactivar usuario
        user = estudiante.usuario
        user.activo = False
        user.save()
        
        return Response({
            "message": "Estudiante dado de baja correctamente (Estado: Baja) y usuario desactivado.",
            "matricula": matricula
        }, status=status.HTTP_200_OK)


# =============================================================================
# TUTORES
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanAccessStudentInfo])
def admin_tutores_list(request):

    """
    GET /api/admin/students/tutores/ - Lista tutores
    POST /api/admin/students/tutores/ - Crear tutor
    """
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        tutores = Tutor.objects.all().order_by('-id')
        result_page = paginator.paginate_queryset(tutores, request)
        serializer = TutorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanAccessStudentInfo])
def admin_tutores_detail(request, pk):
    """
    GET /api/admin/students/tutores/<id>/ - Detalle tutor
    PUT /api/admin/students/tutores/<id>/ - Actualizar tutor
    DELETE /api/admin/students/tutores/<id>/ - Eliminar tutor
    """
    tutor = get_object_or_404(Tutor, pk=pk)
    
    if request.method == 'GET':
        serializer = TutorSerializer(tutor)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TutorSerializer(tutor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        tutor.delete()
        return Response({"message": "Tutor eliminado"}, status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# CONCEPTOS DE PAGO
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanManageFinanzas])
def admin_conceptos_list(request):
    """
    GET /api/admin/conceptos/ - Lista conceptos de pago
    POST /api/admin/conceptos/ - Crear concepto (con generación masiva opcional)
    """
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        conceptos = ConceptoPago.objects.all().order_by('nombre')
        result_page = paginator.paginate_queryset(conceptos, request)
        serializer = ConceptoPagoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ConceptoPagoSerializer(data=request.data)
        if serializer.is_valid():
            concepto = serializer.save()
            _generar_adeudos_masivos(request.data, concepto)
            return Response(ConceptoPagoSerializer(concepto).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageFinanzas])
def admin_conceptos_detail(request, pk):
    """
    GET /api/admin/conceptos/<id>/ - Detalle concepto
    PUT /api/admin/conceptos/<id>/ - Actualizar concepto
    DELETE /api/admin/conceptos/<id>/ - Eliminar concepto
    """
    concepto = get_object_or_404(ConceptoPago, pk=pk)
    
    if request.method == 'GET':
        serializer = ConceptoPagoSerializer(concepto)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ConceptoPagoSerializer(concepto, data=request.data, partial=True)
        if serializer.is_valid():
            concepto = serializer.save()
            _generar_adeudos_masivos(request.data, concepto)
            return Response(ConceptoPagoSerializer(concepto).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        concepto.delete()
        return Response({"message": "Concepto eliminado"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([CanManageFinanzas])
def admin_conceptos_generar_adeudos(request, pk):
    """
    POST /api/admin/conceptos/<id>/generar-adeudos/
    Genera adeudos masivos para el concepto según criterios en el body.
    """
    concepto = get_object_or_404(ConceptoPago, pk=pk)
    count = _generar_adeudos_masivos(request.data, concepto)
    return Response({"message": f"Se generaron {count} adeudos"})


def _generar_adeudos_masivos(data, concepto):
    """Función auxiliar para generar adeudos masivamente"""
    nivel = data.get('aplicar_a_nivel', '')
    grado_id = data.get('aplicar_a_grado')
    grupo_id = data.get('aplicar_a_grupo')
    estrato_id = data.get('aplicar_a_estrato')
    matricula = data.get('aplicar_a_matricula', '')

    if not (nivel or grado_id or grupo_id or estrato_id or matricula):
        return 0

    estudiantes = Estudiante.objects.all()

    if matricula:
        estudiantes = estudiantes.filter(matricula=str(matricula).strip())
    else:
        # Filtrar por inscripciones activas
        inscripciones_path = 'inscripciones'
        filtros_inscripcion = {'inscripciones__ciclo_escolar__activo': True}
        
        if nivel:
            filtros_inscripcion['inscripciones__grupo__grado__nivel_educativo__nombre__icontains'] = nivel
        if grado_id:
            filtros_inscripcion['inscripciones__grupo__grado_id'] = grado_id
        if grupo_id:
            filtros_inscripcion['inscripciones__grupo_id'] = grupo_id
            
        estudiantes = estudiantes.filter(**filtros_inscripcion)

    count = 0
    with transaction.atomic():
        for estudiante in estudiantes:
            # El filtro anterior ya asegura que tengan inscripción activa en el ciclo actual.
            # Aun así, verificamos estado.
            estado = estudiante.get_estado_actual()
            if not estado or not estado.es_estado_activo:
                continue

            if estrato_id:
                estrato_actual = estudiante.get_estrato_actual()
                if not estrato_actual or estrato_actual.id != int(estrato_id):
                    continue

            # Evitar duplicados para el mismo concepto
            if not Adeudo.objects.filter(estudiante=estudiante, concepto=concepto, estatus__in=['pendiente', 'pagado']).exists():
                adeudo = Adeudo(
                    estudiante=estudiante,
                    concepto=concepto,
                    monto_base=concepto.monto_base,
                    estatus='pendiente'
                )
                adeudo.save()
                count += 1
    
    return count


# =============================================================================
# GRADOS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdministrador])
def admin_grados_list(request):
    """
    GET /api/admin/grados/ - Lista grados
    POST /api/admin/grados/ - Crear grado
    """
    if request.method == 'GET':
        grados = Grado.objects.all().order_by('nivel', 'nombre')
        serializer = GradoSerializer(grados, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GradoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdministrador])
def admin_grados_detail(request, pk):
    """
    GET /api/admin/grados/<id>/ - Detalle grado
    PUT /api/admin/grados/<id>/ - Actualizar grado
    DELETE /api/admin/grados/<id>/ - Eliminar grado
    """
    grado = get_object_or_404(Grado, pk=pk)
    
    if request.method == 'GET':
        serializer = GradoSerializer(grado)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GradoSerializer(grado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        grado.delete()
        return Response({"message": "Grado eliminado"}, status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# GRUPOS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdministrador])
def admin_grupos_list(request):
    """
    GET /api/admin/grupos/ - Lista grupos
    POST /api/admin/grupos/ - Crear grupo
    """
    if request.method == 'GET':
        grupos = Grupo.objects.select_related('grado').all().order_by('grado', 'nombre')
        serializer = GrupoSerializer(grupos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GrupoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdministrador])
def admin_grupos_detail(request, pk):
    """
    GET /api/admin/grupos/<id>/ - Detalle grupo
    PUT /api/admin/grupos/<id>/ - Actualizar grupo
    DELETE /api/admin/grupos/<id>/ - Eliminar grupo
    """
    grupo = get_object_or_404(Grupo, pk=pk)
    
    if request.method == 'GET':
        serializer = GrupoSerializer(grupo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GrupoSerializer(grupo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        grupo.delete()
        return Response({"message": "Grupo eliminado"}, status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# ESTRATOS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanManageBecas])
def admin_estratos_list(request):
    """
    GET /api/admin/estratos/ - Lista estratos
    POST /api/admin/estratos/ - Crear estrato
    """
    if request.method == 'GET':
        estratos = Estrato.objects.all().order_by('nombre')
        serializer = EstratoSerializer(estratos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EstratoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageBecas])
def admin_estratos_detail(request, pk):
    """
    GET /api/admin/estratos/<id>/ - Detalle estrato
    PUT /api/admin/estratos/<id>/ - Actualizar estrato
    DELETE /api/admin/estratos/<id>/ - Desactivar estrato (soft delete)
    """
    estrato = get_object_or_404(Estrato, pk=pk)
    
    if request.method == 'GET':
        serializer = EstratoSerializer(estrato)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EstratoSerializer(estrato, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        estrato.activo = False
        estrato.save()
        return Response({"message": "Estrato desactivado"}, status=status.HTTP_200_OK)


# =============================================================================
# ESTADOS DE ESTUDIANTE
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdministrador])
def admin_estados_list(request):
    """
    GET /api/admin/estados/ - Lista estados de estudiante
    POST /api/admin/estados/ - Crear estado
    """
    if request.method == 'GET':
        estados = EstadoEstudiante.objects.all().order_by('nombre')
        serializer = EstadoEstudianteSerializer(estados, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EstadoEstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdministrador])
def admin_estados_detail(request, pk):
    """
    GET /api/admin/estados/<id>/ - Detalle estado
    PUT /api/admin/estados/<id>/ - Actualizar estado
    DELETE /api/admin/estados/<id>/ - Eliminar estado
    """
    estado = get_object_or_404(EstadoEstudiante, pk=pk)
    
    if request.method == 'GET':
        serializer = EstadoEstudianteSerializer(estado)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EstadoEstudianteSerializer(estado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        estado.delete()
        return Response({"message": "Estado eliminado"}, status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# BECAS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanManageBecas])
def admin_becas_list(request):
    """
    GET /api/admin/becas/ - Lista becas
    POST /api/admin/becas/ - Crear beca
    """
    if request.method == 'GET':
        becas = Beca.objects.all().order_by('-valida', 'nombre')
        serializer = BecaSerializer(becas, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BecaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageBecas])
def admin_becas_detail(request, pk):
    """
    GET /api/admin/becas/<id>/ - Detalle beca
    PUT /api/admin/becas/<id>/ - Actualizar beca
    DELETE /api/admin/becas/<id>/ - Eliminar beca
    """
    beca = get_object_or_404(Beca, pk=pk)
    
    if request.method == 'GET':
        serializer = BecaSerializer(beca)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BecaSerializer(beca, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        beca.delete()
        return Response({"message": "Beca eliminada"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([CanManageBecas])
def admin_becas_verificar_vigencia(request):
    """
    POST /api/admin/becas/verificar-vigencia/
    Verifica y marca como vencidas las becas cuya fecha de vencimiento ya pasó.
    """
    updated = Beca.objects.filter(
        fecha_vencimiento__lt=timezone.now().date(),
        valida=True
    ).update(valida=False)
    return Response({"message": f"Se marcaron {updated} becas como vencidas"})


# =============================================================================
# BECAS-ESTUDIANTES (Asignaciones)
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanManageBecas])
def admin_becas_estudiantes_list(request):
    """
    GET /api/admin/becas-estudiantes/ - Lista asignaciones beca-estudiante
    POST /api/admin/becas-estudiantes/ - Asignar beca a estudiante
    """
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        asignaciones = BecaEstudiante.objects.select_related('beca', 'estudiante').all().order_by('-fecha_asignacion')
        result_page = paginator.paginate_queryset(asignaciones, request)
        serializer = BecaEstudianteSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BecaEstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageBecas])
def admin_becas_estudiantes_detail(request, pk):
    """
    GET /api/admin/becas-estudiantes/<id>/ - Detalle asignación
    PUT /api/admin/becas-estudiantes/<id>/ - Actualizar asignación
    DELETE /api/admin/becas-estudiantes/<id>/ - Eliminar asignación
    """
    asignacion = get_object_or_404(BecaEstudiante, pk=pk)
    
    if request.method == 'GET':
        serializer = BecaEstudianteSerializer(asignacion)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BecaEstudianteSerializer(asignacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        asignacion.delete()
        return Response({"message": "Asignación eliminada"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([CanManageBecas])
def admin_becas_estudiantes_retirar_masivo(request):
    """
    POST /api/admin/becas-estudiantes/retirar-masivo/
    Retira becas de múltiples estudiantes.
    Body: {"ids": [1, 2, 3], "motivo": "Fin de ciclo"}
    """
    ids = request.data.get('ids', [])
    motivo = request.data.get('motivo', 'Retiro masivo desde API')
    updated = BecaEstudiante.objects.filter(id__in=ids).update(
        activa=False,
        fecha_retiro=timezone.now(),
        motivo_retiro=motivo
    )
    return Response({"message": f"Se retiraron {updated} asignaciones de beca"})


@api_view(['POST'])
@permission_classes([CanManageBecas])
def admin_becas_estudiantes_activar_masivo(request):
    """
    POST /api/admin/becas-estudiantes/activar-masivo/
    Activa becas para múltiples estudiantes.
    Body: {"ids": [1, 2, 3]}
    """
    ids = request.data.get('ids', [])
    updated = BecaEstudiante.objects.filter(id__in=ids).update(
        activa=True,
        fecha_retiro=None,
        motivo_retiro=None
    )
    return Response({"message": f"Se activaron {updated} asignaciones de beca"})


# =============================================================================
# ADEUDOS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanManageFinanzas])
def admin_adeudos_list(request):
    """
    GET /api/admin/pagos/adeudos/ - Lista adeudos
    POST /api/admin/pagos/adeudos/ - Crear adeudo individual
    """
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        adeudos = Adeudo.objects.select_related('estudiante', 'concepto').all().order_by('-fecha_generacion')
        result_page = paginator.paginate_queryset(adeudos, request)
        serializer = AdeudoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AdeudoCreateSerializer(data=request.data)
        if serializer.is_valid():
            adeudo = serializer.save()
            return Response(AdeudoSerializer(adeudo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageFinanzas])
def admin_adeudos_detail(request, pk):
    """
    GET /api/admin/pagos/adeudos/<id>/ - Detalle adeudo
    PUT /api/admin/pagos/adeudos/<id>/ - Actualizar adeudo
    DELETE /api/admin/pagos/adeudos/<id>/ - Eliminar adeudo
    """
    adeudo = get_object_or_404(Adeudo, pk=pk)
    
    if request.method == 'GET':
        serializer = AdeudoSerializer(adeudo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AdeudoSerializer(adeudo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        adeudo.delete()
        return Response({"message": "Adeudo eliminado"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([CanManageFinanzas])
def admin_adeudos_vencidos(request):
    """
    GET /api/admin/pagos/adeudos/vencidos/
    Lista adeudos vencidos (fecha_vencimiento < hoy y estatus pendiente/parcial).
    """
    paginator = StandardResultsSetPagination()
    vencidos = Adeudo.objects.filter(
        fecha_vencimiento__lt=timezone.now().date(),
        estatus__in=['pendiente', 'parcial']
    ).select_related('estudiante', 'concepto')
    
    result_page = paginator.paginate_queryset(vencidos, request)
    serializer = AdeudoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([CanManageFinanzas])
def admin_adeudos_recalcular(request):
    """
    POST /api/admin/pagos/adeudos/recalcular/
    Recalcula recargos para adeudos específicos o todos los pendientes.
    Body: {"ids": [1, 2, 3]} o vacío para todos
    """
    ids = request.data.get('ids', [])
    if ids:
        adeudos = Adeudo.objects.filter(id__in=ids)
    else:
        adeudos = Adeudo.objects.filter(estatus__in=['pendiente', 'parcial'])
    
    count = 0
    for adeudo in adeudos:
        adeudo.save()  # El save() recalcula recargos
        count += 1
    
    return Response({"message": f"Se recalcularon {count} adeudos"})


@api_view(['POST'])
@permission_classes([CanManageFinanzas])
def admin_adeudos_exentar(request, pk):
    """
    POST /api/admin/pagos/adeudos/<id>/exentar/
    Exenta el recargo de un adeudo específico.
    Body: {"justificacion": "Razón de exención"}
    """
    adeudo = get_object_or_404(Adeudo, pk=pk)
    justificacion = request.data.get('justificacion', '')
    
    adeudo.recargo_exento = True
    adeudo.justificacion_exencion = justificacion
    adeudo.recargo_aplicado = 0
    adeudo.monto_total = adeudo.monto_base - adeudo.descuento_aplicado
    adeudo.save()
    
    return Response(AdeudoSerializer(adeudo).data)


# =============================================================================
# PAGOS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([CanManageFinanzas])
def admin_pagos_list(request):
    """
    GET /api/admin/pagos/ - Lista pagos
    POST /api/admin/pagos/ - Crear pago
    """
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        pagos = Pago.objects.select_related('adeudo', 'adeudo__estudiante', 'adeudo__concepto').all().order_by('-fecha_pago')
        result_page = paginator.paginate_queryset(pagos, request)
        serializer = PagoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PagoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CanManageFinanzas])
def admin_pagos_detail(request, pk):
    """
    GET /api/admin/pagos/<id>/ - Detalle pago
    PUT /api/admin/pagos/<id>/ - Actualizar pago
    DELETE /api/admin/pagos/<id>/ - BLOQUEADO (no se permite eliminar pagos)
    """
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'GET':
        serializer = PagoSerializer(pago)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PagoSerializer(pago, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        return Response({"error": "No se permite eliminar pagos"}, status=status.HTTP_403_FORBIDDEN)


# =============================================================================
# EVALUACIONES (Solo lectura)
# =============================================================================

@api_view(['GET'])
@permission_classes([CanManageBecas])
def admin_evaluaciones_list(request):
    """
    GET /api/admin/students/evaluaciones/ - Lista evaluaciones socioeconómicas
    """
    paginator = StandardResultsSetPagination()
    evaluaciones = EvaluacionSocioeconomica.objects.select_related('estudiante', 'estrato').all().order_by('-fecha_evaluacion')
    result_page = paginator.paginate_queryset(evaluaciones, request)
    serializer = EvaluacionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([CanManageBecas])
def admin_evaluaciones_detail(request, pk):
    """
    GET /api/admin/students/evaluaciones/<id>/ - Detalle evaluación
    """
    evaluacion = get_object_or_404(EvaluacionSocioeconomica, pk=pk)
    serializer = EvaluacionSerializer(evaluacion)
    return Response(serializer.data)

# =============================================================================
# REPORTES FINANCIEROS
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_reporte_ingresos_estrato(request):
    """
    GET /api/admin/reportes/financieros/ingresos-estrato/
    Reporte de ingresos por estrato socioeconómico (mensual y anual).
    """
    anio = request.query_params.get('anio', timezone.now().year)
    mes = request.query_params.get('mes', timezone.now().month)
    
    # Filtrar pagos del año/mes
    pagos = Pago.objects.filter(
        fecha_pago__year=anio
    ).select_related('adeudo__estudiante')
    
    # Agrupar por estrato
    data_anual = {}
    data_mensual = {}
    
    # Inicializar estratos (para que salgan todos aunque sea en 0)
    estratos = Estrato.objects.all()
    for e in estratos:
        data_anual[e.nombre] = 0.00
        data_mensual[e.nombre] = 0.00
    data_anual["Sin Asignar"] = 0.00
    data_mensual["Sin Asignar"] = 0.00
    
    for pago in pagos:
        estudiante = pago.adeudo.estudiante
        estrato = estudiante.get_estrato_actual()
        nombre_estrato = estrato.nombre if estrato else "Sin Asignar"
        
        monto = float(pago.monto)
        
        # Acumulado Anual
        data_anual[nombre_estrato] = data_anual.get(nombre_estrato, 0) + monto
        
        # Acumulado Mensual (si coincide el mes)
        if pago.fecha_pago.month == int(mes):
            data_mensual[nombre_estrato] = data_mensual.get(nombre_estrato, 0) + monto
            
    return Response({
        "anio": anio,
        "mes": mes,
        "ingresos_anuales_por_estrato": data_anual,
        "ingresos_mensuales_por_estrato": data_mensual
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_reporte_recaudacion(request):
    """
    GET /api/admin/reportes/financieros/recaudacion/
    Reporte de recaudación ordinaria vs recargos.
    Basado en el desglose de los ADEUDOS que han sido pagados (parcial o totalmente).
    """
    anio = request.query_params.get('anio', timezone.now().year)
    mes = request.query_params.get('mes', timezone.now().month)
    
    pagos = Pago.objects.filter(
        fecha_pago__year=anio,
        fecha_pago__month=mes
    ).select_related('adeudo')
    
    total_recaudado = 0.00
    total_base_estimado = 0.00
    total_recargos_estimado = 0.00
    
    # Nota: Como el pago es un monto global, haremos una estimación proporcional
    # o simplemente sumaremos lo que el adeudo dice que tiene de recargo 
    # si el pago cubre el total.
    # Estrategia simple: Reportar qué parte de lo cobrado corresponde a recargos
    # asumiendo que el recargo se cobra al final o proporcionalmente?
    # Mejor: Reportar el monto total de recargos GENERADOS vs PAGADOS en el periodo es complejo.
    # Simplificación: Sumar 'recargo_aplicado' de los adeudos que recibieron pago en este mes.
    # Esto no es exacto contablemente pero da una idea.
    
    # Estrategia Alternativa (Más precisa para reporte de "Ingresos"):
    # Considerar que todo pago primero cubre recargos y luego capital (o viceversa).
    # O simplemente reportar el Total Recaudado y, por separado, el Total de Recargos Generados en el mes.
    
    # Vamos a reportar: 
    # 1. Total Cobrado (Real)
    # 2. Total de Recargos que se han cobrado (asumiendo que si se paga el adeudo, se paga el recargo).
    
    for pago in pagos:
        total_recaudado += float(pago.monto)
        
        adeudo = pago.adeudo
        if adeudo.recargo_aplicado > 0:
            # Si el adeudo tiene recargo, ¿cuánto de este pago es recargo?
            # Asumimos prorrata simple para estadistica: 
            # (recargo / total_adeudo) * monto_pago
            if adeudo.monto_total > 0:
                ratio = float(adeudo.recargo_aplicado) / float(adeudo.monto_total)
                recargo_parte = float(pago.monto) * ratio
                total_recargos_estimado += recargo_parte
                total_base_estimado += (float(pago.monto) - recargo_parte)
            else:
                total_base_estimado += float(pago.monto)
        else:
            total_base_estimado += float(pago.monto)
            
    return Response({
        "periodo": f"{mes}/{anio}",
        "total_recaudado": round(total_recaudado, 2),
        "desglose_estimado": {
            "ordinario": round(total_base_estimado, 2),
            "recargos_moratorios": round(total_recargos_estimado, 2)
        },
        "nota": "El desglose es una estimación proporcional basada en los adeudos pagados."
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_estudiantes_adeudos_vencidos(request):
    """
    GET /api/admin/reportes/financieros/adeudos-vencidos/
    Lista estudiantes con deuda vencida total.
    """
    # Estudiantes con al menos un adeudo vencido
    estudiantes_deudores = Estudiante.objects.filter(
        adeudo__estatus='vencido'
    ).distinct()
    
    data = []
    for est in estudiantes_deudores:
        adeudos_vencidos = est.adeudo_set.filter(estatus='vencido')
        total_vencido = sum(a.monto_total - a.monto_pagado for a in adeudos_vencidos)
        
        grupo_str = "S/A"
        if est.grupo:
             grupo_str = f"{est.grupo.grado.nombre} {est.grupo.nombre}"
             
        data.append({
            "matricula": est.matricula,
            "nombre": f"{est.nombre} {est.apellido_paterno}",
            "grupo": grupo_str,
            "cantidad_adeudos_vencidos": adeudos_vencidos.count(),
            "monto_total_vencido": total_vencido
        })
        
    return Response(data)

# =============================================================================
# REPORTES ACADÉMICOS Y EXPORTACIONES
# =============================================================================

from .utils_export import generar_excel_estudiantes, generar_pdf_estudiantes, generar_excel_aspirantes
from admissions.models import Aspirante

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_estadisticas_academicas(request):
    """
    GET /api/admin/reportes/academicos/estadisticas/
    Estadísticas de inscripciones, bajas y reinscripciones.
    """
    # 1. Total Inscritos Actuales (Estudiantes activos)
    total_activos = Estudiante.objects.filter(
        historialestadosestudiante__estado__es_estado_activo=True
    ).distinct().count()
    
    # Inscritos en ciclo actual
    inscritos_ciclo_actual = Inscripcion.objects.filter(ciclo_escolar__activo=True).count()
    
    # 2. Bajas (en el último año o ciclo activo)
    bajas_totales = HistorialEstadosEstudiante.objects.filter(
        estado__nombre__icontains='BAJA'
    ).count()
    
    # 3. Reinscripciones (Simple: total activos - nuevos ingreso)
    # Definición aproximada: Inscripciones en ciclo actual que tienen inscripciones previas
    reinscritos = 0
    inscripciones_actuales = Inscripcion.objects.filter(ciclo_escolar__activo=True).select_related('estudiante')
    if inscripciones_actuales.exists():
        # Tomamos una muestra o lo hacemos query
        # Estudiantes en ciclo actual que tienen una inscripción en un ciclo DIFERENTE (y anterior)
        estudiantes_ids = inscripciones_actuales.values_list('estudiante_id', flat=True)
        reinscritos = Inscripcion.objects.filter(
            estudiante_id__in=estudiantes_ids
        ).exclude(ciclo_escolar__activo=True).values('estudiante').distinct().count()
            
    return Response({
        "inscritos_ciclo_actual": inscritos_ciclo_actual,
        "estudiantes_activos_totales": total_activos,
        "bajas_historicas": bajas_totales,
        "reinscripciones_ciclo_actual": reinscritos
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_exportar_estudiantes(request):
    """
    GET /api/admin/exportar/estudiantes/?format=excel|pdf
    Exporta el listado de estudiantes.
    """
    fmt = request.query_params.get('format', 'excel')
    
    # Obtener estudiantes
    queryset = Estudiante.objects.select_related('usuario').prefetch_related(
        models.Prefetch(
            'inscripciones',
            queryset=Inscripcion.objects.filter(ciclo_escolar__activo=True).select_related('grupo__grado__nivel_educativo'),
            to_attr='active_enrollment'
        )
    ).all().order_by('matricula')
    
    if fmt == 'pdf':
        buffer = generar_pdf_estudiantes(queryset)
        if not buffer:
            return Response({"error": "Librería ReportLab no disponible"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.pdf"'
        return response
    else:
        # Excel default
        buffer = generar_excel_estudiantes(queryset)
        if not buffer:
             return Response({"error": "Librería OpenPyXL no disponible"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.xlsx"'
        return response


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_exportar_aspirantes(request):
    """
    GET /api/admin/exportar/aspirantes/
    Exporta el listado de aspirantes en Excel.
    """
    queryset = Aspirante.objects.select_related('user').all().order_by('apellido_paterno')
    
    buffer = generar_excel_aspirantes(queryset)
    if not buffer:
         return Response({"error": "Librería OpenPyXL no disponible"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="aspirantes.xlsx"'
    return response

# =============================================================================
# PASSWORD RESET FLOW
# =============================================================================

class PasswordResetRequestView(APIView):
    """
    Paso 1: Solicitar código de restablecimiento.
    Busca en Estudiantes (User) o Aspirantes (AdmissionUser).
    Genera código de 6 dígitos y (simula) envío por correo.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Buscar en USUARIOS (Estudiantes active)
        try:
            user = User.objects.get(email=email, role='estudiante')
            code = f"{random.randint(100000, 999999)}"
            user.mfa_code = code
            user.mfa_expires_at = timezone.now() + timedelta(minutes=15)
            user.save(update_fields=['mfa_code', 'mfa_expires_at'])
            
            print(f"\\n[MOCK EMAIL] Password Reset Code para ESTUDIANTE {email}: {code}\\n")
            response_data = {'message': f'Si el correo existe, se ha enviado un código de verificación.'}
            if settings.DEBUG:
                response_data['code_debug'] = code
            return Response(response_data)
            
        except User.DoesNotExist:
            pass
            
        # 2. Buscar en ASPIRANTES
        try:
            adm_user = AdmissionUser.objects.get(email=email)
            code = f"{random.randint(100000, 999999)}"
            
            # Usar VerificationCode (reutilizando modelo existente en admissions)
            VerificationCode.objects.update_or_create(
                email=email,
                defaults={
                    'code': code,
                    'created_at': timezone.now(),
                    'expires_at': timezone.now() + timedelta(minutes=15),
                    'is_verified': False
                }
            )
            
            print(f"\\n[MOCK EMAIL] Password Reset Code para ASPIRANTE {email}: {code}\\n")
            return Response({'message': f'Si el correo existe, se ha enviado un código de verificación.'})
            
        except AdmissionUser.DoesNotExist:
            pass
            
        # Retornar éxito genérico para evitar enumeración de usuarios
        return Response({'message': f'Si el correo existe, se ha enviado un código de verificación.'})


class PasswordResetVerifyView(APIView):
    """
    Paso 2: Verificar código recibio por email.
    Retorna un 'reset_token' (JWT temporal) si es válido.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        if not email or not code:
            return Response({'error': 'Email y código requeridos'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 1. Verificar Estudiante
        try:
            user = User.objects.get(email=email, role='estudiante')
            if user.mfa_code == code and user.mfa_expires_at and user.mfa_expires_at > timezone.now():
                # Código válido
                token_payload = {
                    'email': email,
                    'type': 'password_reset',
                    'user_type': 'student',
                    'exp': datetime.utcnow() + timedelta(minutes=15)
                }
                reset_token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'message': 'Código válido', 'reset_token': reset_token})
        except User.DoesNotExist:
            pass
            
        # 2. Verificar Aspirante
        try:
            # Check VerificationCode table
            vc = VerificationCode.objects.filter(email=email, code=code, is_verified=False).last()
            if vc and vc.is_valid():
                # Código válido
                token_payload = {
                    'email': email,
                    'type': 'password_reset',
                    'user_type': 'aspirante',
                    'exp': datetime.utcnow() + timedelta(minutes=15)
                }
                reset_token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
                
                # Marcar como verificado para que no se reuse el mismísimo codigo inmediatamente (opcional)
                vc.is_verified = True
                vc.save()
                
                return Response({'message': 'Código válido', 'reset_token': reset_token})
        except Exception as e:
            pass
            
        return Response({'error': 'Código inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    Paso 3: Cambiar la contraseña usando el reset_token.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        reset_token = request.data.get('reset_token')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not reset_token or not new_password:
            return Response({'error': 'Token y nueva contraseña requeridos'}, status=status.HTTP_400_BAD_REQUEST)
            
        if new_password != confirm_password:
            return Response({'error': 'Las contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            payload = jwt.decode(reset_token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'password_reset':
                raise jwt.InvalidTokenError
                
            email = payload.get('email')
            user_type = payload.get('user_type')
            
            if user_type == 'student':
                user = User.objects.get(email=email)
                user.set_password(new_password)
                # Limpiar MFA code
                user.mfa_code = None
                user.mfa_expires_at = None
                user.save()
                return Response({'message': 'Contraseña actualizada exitosamente (Estudiante)'})
                
            elif user_type == 'aspirante':
                adm_user = AdmissionUser.objects.get(email=email)
                adm_user.set_password(new_password)
                adm_user.save()
                return Response({'message': 'Contraseña actualizada exitosamente (Aspirante)'})
                
        except jwt.ExpiredSignatureError:
            return Response({'error': 'El token ha expirado'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error al actualizar contraseña: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
