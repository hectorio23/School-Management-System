from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.models import Group

from academico.models import Maestro, NivelEducativo
from academico.serializers import MaestroSerializer
from academico.permissions import IsAdministradorEscolar
from users.models import User

@api_view(['GET', 'POST'])
@permission_classes([IsAdministradorEscolar])
def admin_maestros_list_create(request):
    """
    GET: Listar maestros del nivel del admin.
    POST: Crear nuevo maestro (y usuario) para este nivel.
    """
    admin = request.user.admin_escolar_perfil
    
    if request.method == 'GET':
        queryset = Maestro.objects.filter(
            nivel_educativo=admin.nivel_educativo,
            activo=True
        ).annotate(
            num_asignaciones=Count('asignaciones', filter=Q(asignaciones__activa=True))
        ).order_by('nombre')
        serializer = MaestroSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Custom logic to create User + Maestro
        data = request.data
        email = data.get('email')
        password = data.get('password')
        nombre = data.get('nombre')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno', '')
        telefono = data.get('telefono', '')
        fecha_contratacion = data.get('fecha_contratacion')

        if User.objects.filter(email=email).exists():
            return Response({"message": "El email ya está registrado"}, status=400)

        try:
            user = User.objects.create_user(email=email, password=password, role='maestro')
            
            # Asignar grupo 'Maestros'
            group, _ = Group.objects.get_or_create(name='Maestros')
            user.groups.add(group)

            maestro = Maestro.objects.create(
                usuario=user,
                nivel_educativo=admin.nivel_educativo,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                telefono=telefono,
                fecha_contratacion=fecha_contratacion
            )
            
            return Response(MaestroSerializer(maestro).data, status=201)
        except Exception as e:
            return Response({"message": str(e)}, status=400)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdministradorEscolar])
def admin_maestro_detail(request, pk):
    """
    PUT: Actualizar datos del maestro.
    DELETE: Desactivar maestro (soft delete).
    """
    admin = request.user.admin_escolar_perfil
    maestro = get_object_or_404(Maestro, pk=pk, nivel_educativo=admin.nivel_educativo)

    if request.method == 'PUT':
        serializer = MaestroSerializer(maestro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        maestro.activo = False
        maestro.save()
        maestro.usuario.is_active = False
        maestro.usuario.save()
        return Response({"message": "Maestro desactivado correctamente"})
