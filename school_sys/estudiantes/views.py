"""
Vistas para el endpoint de información del estudiante.
Refactorizado a Function Based Views (FBV) con decoradores.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Estudiante, Tutor, EstudianteTutor
from .serializers import EstudianteInfoSerializer, TutorUpdateSerializer
from .permissions import IsEstudiante


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEstudiante]) 
def estudiante_info_view(request):
    """
    GET /students/info/
    
    Retorna la información del estudiante autenticado.
    Solo accesible para usuarios con rol 'estudiante'.
    """

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
