from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count

from academico.models import Materia, Grado
from academico.serializers import MateriaSerializer
from academico.permissions import IsAdministradorEscolar

@api_view(['GET', 'POST'])
@permission_classes([IsAdministradorEscolar])
def admin_materias_list_create(request):
    """
    GET: Listar materias del nivel.
    POST: Crear materia.
    """
    admin = request.user.admin_escolar_perfil
    
    if request.method == 'GET':
        queryset = Materia.objects.filter(
            grado__nivel_educativo=admin.nivel_educativo,
            activa=True
        ).select_related('grado', 'programa_educativo').order_by('grado__numero_grado', 'orden', 'nombre')
        serializer = MateriaSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        grado_id = data.get('grado')
        grado = get_object_or_404(Grado, pk=grado_id)
        
        if grado.nivel_educativo != admin.nivel_educativo:
             return Response({"message": "No tiene permiso para crear materias en este grado"}, status=403)

        serializer = MateriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdministradorEscolar])
def admin_materia_detail(request, pk):
    admin = request.user.admin_escolar_perfil
    materia = get_object_or_404(Materia, pk=pk, grado__nivel_educativo=admin.nivel_educativo)

    if request.method == 'PUT':
        serializer = MateriaSerializer(materia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        materia.activa = False
        materia.save()
        return Response({"message": "Materia desactivada"})

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_programas_list(request):
    """Listar programas educativos del nivel."""
    admin = request.user.admin_escolar_perfil
    from academico.models import ProgramaEducativo
    programas = ProgramaEducativo.objects.filter(nivel_educativo=admin.nivel_educativo).order_by('-activo', '-fecha_inicio')
    data = [{"id": p.id, "nombre": p.nombre, "activo": p.activo} for p in programas]
    return Response(data)
