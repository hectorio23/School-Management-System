"""
Vistas para el endpoint de información del estudiante.
Refactorizado a Function Based Views (FBV) con decoradores.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Estudiante, Tutor, EstudianteTutor, EvaluacionSocioeconomica, Estrato
from .serializers import EstudianteInfoSerializer, TutorUpdateSerializer, EstudioSocioeconomicoCreateSerializer
from .permissions import IsEstudiante
from django.http import HttpResponse
from django.shortcuts import render
import os
from django.utils import timezone
from datetime import timedelta


"""Aqui es donde va la direccón del dashboard en caso de que 
   no se use un framework para el manejo de Front-End. 
   los html irán en la carpeta llamada templates/
   los recursos de css y javascript, van en la carpeta static
   en sus respectivos lugares
"""
def dashboard(request):
    
    # return render(request, "dashboars de estudiante")
    return render(request, "./dashboard.html")


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEstudiante]) 
def estudiante_info_view(request):
    """
    GET /students/info/
    
    Retorna la información del estudiante autenticado.
    Solo accesible para usuarios con rol 'estudiante'.
    """

    print(request.user)

    try:
        # Obtener el perfil de estudiante del usuario autenticado
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {"error": "[X] - No se encontró el perfil de estudiante asociado a este usuario."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = EstudianteInfoSerializer(estudiante)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsEstudiante])
def tutores_update_view(request):
    """
    PUT /students/tutores/
    
    Actualiza la información de todos los tutores del estudiante autenticado.
    Recibe un array de tutores con su información actualizada.
    Solo puede actualizar tutores que pertenezcan al estudiante.
    """
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {"error": "[X] - No se encontró el perfil de estudiante asociado a este usuario."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    tutores_data = request.data.get('tutores', [])

    for tutor in tutores_data:
        if not all(tutor):
            return Response(
                { "error": "[X] - Campos incompletos." },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if not isinstance(tutores_data, list):
        return Response(
            {"error": "[X] - Se esperaba un array de tutores en el campo 'tutores'."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not tutores_data:
        return Response(
            {"error": "[X] - Debe proporcionar al menos un tutor para actualizar."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener IDs de tutores que pertenecen al estudiante
    tutores_permitidos = set(
        EstudianteTutor.objects.filter(
            estudiante=estudiante,
            activo=True
        ).values_list('tutor_id', flat=True)
    )
    
    errores = []
    tutores_actualizados = []
    
    for idx, tutor_data in enumerate(tutores_data):
        tutor_id = tutor_data.get('tutor_id') or tutor_data.get('id')
        
        if not tutor_id:
            errores.append({
                "index": idx,
                "error": "[X] - Falta el campo 'tutor_id'."
            })
            continue
        
        # Verificar que el tutor pertenezca al estudiante
        if tutor_id not in tutores_permitidos:
            errores.append({
                "index": idx,
                "tutor_id": tutor_id,
                "error": "[X] - No tienes permiso para actualizar este tutor."
            })
            continue
        
        try:
            tutor = Tutor.objects.get(id=tutor_id)
        except Tutor.DoesNotExist:
            errores.append({
                "index": idx,
                "tutor_id": tutor_id,
                "error": "[X] - Tutor no encontrado."
            })
            continue
        
        serializer = TutorUpdateSerializer(tutor, data=tutor_data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            tutores_actualizados.append(serializer.data)
        else:
            errores.append({
                "index": idx,
                "tutor_id": tutor_id,
                "errors": serializer.errors
            })
    
    if errores:
        return Response({
            "message": "[+] - Algunos tutores no pudieron ser actualizados por información incompleta.",
            "actualizados": tutores_actualizados,
            "errores": errores
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        "message": "[+] - Todos los tutores proporcionadosfueron actualizados correctamente.",
        "tutores": tutores_actualizados
    }, status=status.HTTP_200_OK)


def guardar_documentos_extra(estudiante, files):
    """
    Función placeholder para guardar documentos extra (Acta, CURP).
    Será implementada posteriormente.
    """
    # TODO: Implementar lógica de guardado de documentos
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEstudiante])
def create_estudio_socioeconomico_view(request):
    """
    POST /students/estudio-socioeconomico/
    
    Crea una nueva evaluación socioeconómica para el estudiante.
    
    Validaciones:
    - Tiempo mínimo entre estudios (configurado en MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES)
    - Cambios de estrato > 2 niveles requieren aprobación especial
    
    Calcula el estrato automáticamente basado en el ingreso mensual (Cambiar en producción):
    - Ingreso <= 10,000 -> Estrato B
    - Ingreso > 10,000 -> Estrato A
    """
    
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {"error": "[X] - No se encontró el perfil de estudiante asociado a este usuario."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Validar tiempo desde último estudio
    meses_requeridos = int(os.getenv('MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES', '1'))
    fecha_limite = timezone.now() - timedelta(days=30 * meses_requeridos)
    
    ultimo_estudio = EvaluacionSocioeconomica.objects.filter(
        estudiante=estudiante,
        fecha_evaluacion__gte=fecha_limite
    ).first()
    
    if ultimo_estudio:
        dias_restantes = (ultimo_estudio.fecha_evaluacion + timedelta(days=30 * meses_requeridos) - timezone.now()).days
        return Response({
            "error": f"Debe esperar {meses_requeridos} mes(es) entre estudios socioeconómicos.",
            "ultimo_estudio": ultimo_estudio.fecha_evaluacion.strftime("%Y-%m-%d"),
            "dias_restantes": max(0, dias_restantes)
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = EstudioSocioeconomicoCreateSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        
        # Calcular Estrato sugerido
        ingreso = validated_data.get('ingreso_mensual')
        
        # Definir rangos de estrato por ingreso
        # TODO: Esto debería venir de la tabla Estrato o configuración
        if ingreso <= 5000:
            nombre_estrato = 'C'
        elif ingreso <= 10000:
            nombre_estrato = 'B'
        else:
            nombre_estrato = 'A'
        
        try:
            estrato_sugerido = Estrato.objects.get(nombre=nombre_estrato)
        except Estrato.DoesNotExist:
            # Fallback: buscar el primer estrato activo
            estrato_sugerido = Estrato.objects.filter(activo=True).first()
            if not estrato_sugerido:
                return Response(
                    {"error": f"[X] - El estrato '{nombre_estrato}' no está configurado en el sistema."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # Detectar cambio grande de estrato (> 2 niveles)
        requiere_aprobacion_especial = False
        estrato_actual = estudiante.get_estrato_actual()
        
        if estrato_actual:
            # Mapeo de estratos a niveles numéricos para comparación
            niveles = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
            nivel_actual = niveles.get(estrato_actual.nombre, 0)
            nivel_nuevo = niveles.get(estrato_sugerido.nombre, 0)
            
            diferencia = abs(nivel_actual - nivel_nuevo)
            if diferencia > 2:
                requiere_aprobacion_especial = True
            
        # Extraer archivos para procesarlos aparte
        acta = validated_data.pop('acta_nacimiento', None)
        curp = validated_data.pop('curp', None)

        ## Guardar archivos
        # TODO: Hacer función que gestione el almacenamiento de los archivos
        # por cada estudiante
        
        # files_to_save = {}
        # if acta:
        #     files_to_save['acta_nacimiento'] = acta
        # if curp:
        #     files_to_save['curp'] = curp
            
        # if files_to_save:
        #     guardar_documentos_extra(estudiante, files_to_save)
            
        # Crear evaluación
        evaluacion = EvaluacionSocioeconomica.objects.create(
            estudiante=estudiante,
            estrato=None if requiere_aprobacion_especial else estrato_sugerido,  # No asignar si requiere aprobación
            estrato_sugerido=estrato_sugerido,
            ingreso_mensual=ingreso,
            tipo_vivienda=validated_data.get('tipo_vivienda'),
            miembros_hogar=validated_data.get('miembros_hogar'),
            documentos_json='{}',  # JSON vacío por defecto
            requiere_aprobacion_especial=requiere_aprobacion_especial,
            aprobado=None if requiere_aprobacion_especial else True,  # Pendiente si requiere aprobación
            # Guardar snapshot del porcentaje de descuento al momento de la evaluación
            porcentaje_descuento_snapshot=estrato_sugerido.porcentaje_descuento if estrato_sugerido else None
        )
        
        response_data = {
            "message": "[+] - Evaluación socioeconómica registrada correctamente.",
            "estrato_sugerido": estrato_sugerido.nombre,
            "requiere_aprobacion_especial": requiere_aprobacion_especial,
        }
        
        if requiere_aprobacion_especial:
            response_data["NOTA"] = "El cambio de estrato es significativo (más de 2 niveles). Requiere aprobación del administrador."
        else:
            response_data["NOTA"] = "El administrador tiene que validar el Estrato socioeconómico"
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

