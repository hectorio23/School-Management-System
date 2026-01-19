from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.views import APIView

from estudiantes.models import Estudiante, Tutor, EvaluacionSocioeconomica
from pagos.models import Pago, Adeudo

# Import from the new admin serializers file
from .serializers_admin import (
    TutorSerializer, 
    EstudianteAdminSerializer, 
    EstudianteUpdateSerializer, 
    PagoSerializer, 
    AdeudoSerializer, 
    AdeudoCreateSerializer,
    EvaluacionSerializer
)

# Create your views here.

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

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_student_list(request):
    """
    Retorna lista de estudiantes paginada (60 por página).
    Solo info esencial: matricula, apellidos, grado, grupo, estrato, estatus.
    """
    paginator = StudentPagination()
    # Optimizamos queries con select_related para evitar N+1 en grupo/grado
    students = Estudiante.objects.select_related('grupo', 'grupo__grado').order_by('matricula')
    
    result_page = paginator.paginate_queryset(students, request)
    
    data = []
    for s in result_page:
        # Manejo seguro de atributos nulos
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
@permission_classes([IsAdminUser])
def admin_student_detail(request, matricula):
    """
    Retorna TODO sobre un alumno: info personal, tutores, historial, deudas, etc.
    """
    try:
        student = Estudiante.objects.select_related('grupo', 'grupo__grado', 'usuario').get(matricula=matricula)
    except Estudiante.DoesNotExist:
        return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # 1. Info Básica
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

    # 2. Tutores
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

    # 3. Historial de Estados
    historial_estados = student.historialestadosestudiante_set.select_related('estado').order_by('-fecha_creacion')
    estados_data = []
    for h in historial_estados:
        estados_data.append({
            "estado": h.estado.nombre,
            "fecha": h.fecha_creacion,
            "justificacion": h.justificacion
        })

    # 4. Evaluaciones Socioeconomicas
    evaluaciones = student.evaluacionsocioeconomica_set.select_related('estrato').order_by('-fecha_evaluacion')
    evaluaciones_data = []
    for eva in evaluaciones:
        evaluaciones_data.append({
            "fecha": eva.fecha_evaluacion,
            "estrato_resultante": eva.estrato.nombre if eva.estrato else "Pendiente/Nulo",
            "ingreso_mensual": eva.ingreso_mensual,
            "aprobado": eva.aprobado
        })

    # 5. Estado Actual (Resumen)
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

# --- NEW VIEWSETS FOR CRUD ---

# --- TUTORS VIEWS ---
class AdminTutorViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Tutores.
    GET: Lista paginada (150)
    POST: Crear
    PUT: Actualizar
    DELETE: Eliminar
    """
    queryset = Tutor.objects.all().order_by('-id')
    serializer_class = TutorSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

# --- ADEUDOS / DEBTS VIEWS ---
class AdminAdeudoViewSet(viewsets.ModelViewSet):
    """
    CRUD para Adeudos.
    POST: Usa lógica especial para calcular descuentos.
    """
    queryset = Adeudo.objects.select_related('estudiante', 'concepto').all().order_by('-fecha_generacion')
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AdeudoCreateSerializer
        return AdeudoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adeudo = serializer.save()
        read_serializer = AdeudoSerializer(adeudo)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

# --- PAGOS VIEWS ---
class AdminPagoViewSet(viewsets.ModelViewSet):
    """
    CRUD para Pagos. (Delete bloqueado por seguridad/requerimiento)
    """
    queryset = Pago.objects.select_related('adeudo', 'adeudo__estudiante', 'adeudo__concepto').all().order_by('-fecha_pago')
    serializer_class = PagoSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def destroy(self, request, *args, **kwargs):
        return Response({"error": "No se permite eliminar pagos"}, status=status.HTTP_403_FORBIDDEN)

# --- EVALUACIONES VIEWS ---
class AdminEvaluacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo lectura para historial, aunque podría ser CRUD si se requiere.
    """
    queryset = EvaluacionSocioeconomica.objects.select_related('estudiante', 'estrato').all().order_by('-fecha_evaluacion')
    serializer_class = EvaluacionSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination


# --- STUDENT CRUD EXTRA (Create/Update) ---
class AdminStudentOpsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Crear usuario + estudiante trasnacionalmente"""
        serializer = EstudianteAdminSerializer(data=request.data)
        if serializer.is_valid():
            estudiante = serializer.save()
            return Response(EstudianteAdminSerializer(estudiante).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminStudentDetailOpsView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, matricula):
        estudiante = get_object_or_404(Estudiante, matricula=matricula)
        serializer = EstudianteUpdateSerializer(estudiante, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, matricula):
        """Soft delete (Baja)"""
        estudiante = get_object_or_404(Estudiante, matricula=matricula)
        # Dar de baja: desactivar usuario
        estudiante.usuario.activo = False
        estudiante.usuario.save()
        return Response({"message": "Alumno dado de baja (usuario desactivado)"}, status=status.HTTP_200_OK)
