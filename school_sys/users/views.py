from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.utils import timezone

from estudiantes.models import (
    Estudiante, Tutor, EvaluacionSocioeconomica, 
    Grado, Grupo, Estrato, EstadoEstudiante, Beca, BecaEstudiante,
    HistorialEstadosEstudiante
)
from pagos.models import Pago, Adeudo, ConceptoPago

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
@permission_classes([AllowAny])
def admin_student_list(request):
    """
    GET /api/admin/students/
    Retorna lista de estudiantes paginada (60 por página).
    """
    paginator = StudentPagination()
    students = Estudiante.objects.select_related('grupo', 'grupo__grado').order_by('matricula')
    
    result_page = paginator.paginate_queryset(students, request)
    
    data = []
    for s in result_page:
        nombre_grado = "S/A"
        nombre_grupo = "S/A"
        
        if s.grupo:
            nombre_grupo = s.grupo.nombre
            if s.grupo.grado:
                nombre_grado = f"{s.grupo.grado.nombre} {s.grupo.grado.nivel}"

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
@permission_classes([AllowAny])
def admin_student_detail(request, matricula):
    """
    GET /api/admin/students/<matricula>/
    Retorna TODO sobre un alumno: info personal, tutores, historial, deudas, etc.
    """
    try:
        student = Estudiante.objects.select_related('grupo', 'grupo__grado', 'usuario').get(matricula=matricula)
    except Estudiante.DoesNotExist:
        return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    info_basica = {
        "matricula": student.matricula,
        "nombre_completo": f"{student.nombre} {student.apellido_paterno} {student.apellido_materno}",
        "nombres": student.nombre,
        "apellido_paterno": student.apellido_paterno,
        "apellido_materno": student.apellido_materno,
        "curp": student.usuario.username, 
        "email": student.usuario.email,
        "direccion": student.direccion,
        "grupo": str(student.grupo) if student.grupo else "Sin Grupo",
        "grado": str(student.grupo.grado) if (student.grupo and student.grupo.grado) else "Sin Grado",
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
    balance = student.get_balance_total()

    data = {
        "informacion_personal": info_basica,
        "resumen_academico": {
            "estrato_actual": estrato_actual.nombre if estrato_actual else "N/A",
            "estado_escolar": estado_actual.nombre if estado_actual else "N/A",
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
        if nivel:
            estudiantes = estudiantes.filter(grupo__grado__nivel=nivel)
        if grado_id:
            estudiantes = estudiantes.filter(grupo__grado_id=grado_id)
        if grupo_id:
            estudiantes = estudiantes.filter(grupo_id=grupo_id)

    count = 0
    with transaction.atomic():
        for estudiante in estudiantes:
            estado = estudiante.get_estado_actual()
            if not estado or not estado.es_estado_activo:
                continue

            if estrato_id:
                estrato_actual = estudiante.get_estrato_actual()
                if not estrato_actual or estrato_actual.id != int(estrato_id):
                    continue

            if not Adeudo.objects.filter(estudiante=estudiante, concepto=concepto).exists():
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def admin_evaluaciones_detail(request, pk):
    """
    GET /api/admin/students/evaluaciones/<id>/ - Detalle evaluación
    """
    evaluacion = get_object_or_404(EvaluacionSocioeconomica, pk=pk)
    serializer = EvaluacionSerializer(evaluacion)
    return Response(serializer.data)
