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


"""Aqui es donde va la direccón del dashboard en caso de que 
   no se use un framework para el manejo de Front-End. 
   los html irán en la carpeta llamada templates/
   los recursos de css y javascript, van en la carpeta static
   en sus respectivos lugares
"""
def dashboard(request):
    
    # return render(request, "./turuta del dashboars")
    return HttpResponse("<h1><center>Hola XD, yo soy el dashboard</center></h1>")


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

    serializer = EstudioSocioeconomicoCreateSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        
        # Calcular Estrato
        ingreso = validated_data.get('ingreso_mensual')
        nombre_estrato = 'B' if ingreso <= 10000 else 'A'
        
        try:
            estrato = Estrato.objects.get(nombre=nombre_estrato)
        except Estrato.DoesNotExist:
             return Response(
                {"error": f"[X] - El estrato '{nombre_estrato}' no está configurado en el sistema."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
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
            estrato=estrato,
            ingreso_mensual=ingreso,
            tipo_vivienda=validated_data.get('tipo_vivienda'),
            miembros_hogar=validated_data.get('miembros_hogar'),
        )
        
        return Response({
            "message": "[+] - Evaluación socioeconómica registrada correctamente.",
            "estrato_sugerido": estrato.nombre,
            "NOTA": "El administrador tiene que validar el Estrato socioeconómico",
            # "descuento": estrato.porcentaje_descuento
        }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

