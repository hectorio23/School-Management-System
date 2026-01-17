from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from estudiantes.models import (
    Estudiante, 
    Tutor, 
    EstadoEstudiante, 
    HistorialEstadosEstudiante
)
from pagos.models import Pago
from .serializers_admin import (
    TutorSerializer, 
    EstudianteAdminSerializer, 
    EstudianteUpdateSerializer, 
    PagoSerializer
)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class LargePagination(PageNumberPagination):
    page_size = 150
    page_size_query_param = 'page_size'
    max_page_size = 500


# ----- TUTORES -----

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_tutor_list(request):
    """Lista o crea tutores"""
    if request.method == 'GET':
        tutors = Tutor.objects.all().order_by('apellido_paterno')
        paginator = LargePagination()
        result_page = paginator.paginate_queryset(tutors, request)
        serializer = TutorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_tutor_detail(request, pk):
    """Ver, editar o eliminar un tutor"""
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
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----- ESTUDIANTES -----

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_student_list(request):
    """Lista o crea estudiantes (POST crea User + Estudiante en transaccion)"""
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 60
        
        # select_related para evitar N+1
        students = Estudiante.objects.select_related('grupo', 'grupo__grado').order_by('matricula')
        result_page = paginator.paginate_queryset(students, request)

        data = []
        for s in result_page:
            # por si grupo o grado son null
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

    elif request.method == 'POST':
        serializer = EstudianteAdminSerializer(data=request.data)
        if serializer.is_valid():
            estudiante = serializer.save()
            return Response({"matricula": estudiante.matricula}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_student_detail(request, pk):
    """Detalle, update o baja de estudiante (DELETE = soft delete)"""
    if request.method == 'GET':
        try:
            student = Estudiante.objects.select_related('grupo', 'grupo__grado', 'usuario').get(matricula=pk)
        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # info basica
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
        }

        # tutores
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

        # historial
        historial_estados = student.historialestadosestudiante_set.select_related('estado').order_by('-fecha_creacion')
        estados_data = []
        for h in historial_estados:
            estados_data.append({
                "estado": h.estado.nombre,
                "fecha": h.fecha_creacion,
                "justificacion": h.justificacion
            })

        # evals socioeconomicas
        evaluaciones = student.evaluacionsocioeconomica_set.select_related('estrato').order_by('-fecha_evaluacion')
        evaluaciones_data = []
        for eva in evaluaciones:
            evaluaciones_data.append({
                "fecha": eva.fecha_evaluacion,
                "estrato_resultante": eva.estrato.nombre if eva.estrato else "Pendiente/Nulo",
                "ingreso_mensual": eva.ingreso_mensual,
                "aprobado": eva.aprobado
            })

        # resumen
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

    elif request.method == 'PUT':
        student = get_object_or_404(Estudiante, matricula=pk)
        serializer = EstudianteUpdateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # no elimina, solo cambia estado a Baja
        student = get_object_or_404(Estudiante, matricula=pk)
        
        # buscar estado Baja en el catalogo
        try:
            # buscar cualquier estado con 'Baja' en el nombre
            estado_baja = EstadoEstudiante.objects.filter(nombre__icontains='Baja').first()
            if not estado_baja:
                 return Response({"error": "No existe un estado de 'Baja' configurado en el sistema"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # meter al historial
            HistorialEstadosEstudiante.objects.create(
                estudiante=student,
                estado=estado_baja,
                justificacion="Baja administrativa por eliminación"
            )
            
            # desactivar usuario tambien
            student.usuario.activo = False
            student.usuario.save()

            return Response({"message": f"Estudiante dado de baja. Nuevo estado: {estado_baja.nombre}"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----- PAGOS -----

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_pago_list(request):
    """Lista o crea pagos"""
    if request.method == 'GET':
        pagos = Pago.objects.all().order_by('-fecha_pago')
        paginator = StandardPagination()
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
@permission_classes([IsAdminUser])
def admin_pago_detail(request, pk):
    """Ver o editar pago (DELETE bloqueado)"""
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
        return Response(
            {"detail": "La eliminación de pagos no está permitida. Use cancelaciones o ajustes."}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
