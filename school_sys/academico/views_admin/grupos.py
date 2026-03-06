from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count

from academico.models import Grupo, CicloEscolar
from academico.serializers import GrupoSerializer
from academico.permissions import IsAdministradorEscolar
from estudiantes.models import Grado

@api_view(['GET', 'POST'])
@permission_classes([IsAdministradorEscolar])
def admin_grupos_list_create(request):
    """
    GET: Listar grupos del nivel en el CICLO ACTIVO.
    POST: Crear grupo en ciclo activo.
    """
    admin = request.user.admin_escolar_perfil
    
    if request.method == 'GET':
        queryset = Grupo.objects.filter(
            grado__nivel_educativo=admin.nivel_educativo,
            ciclo_escolar__activo=True
        ).annotate(
            num_estudiantes=Count('inscripciones', filter=Q(inscripciones__estatus='activo'), distinct=True),
            num_materias=Count('asignaciones_maestro', filter=Q(asignaciones_maestro__activa=True), distinct=True)
        ).select_related('grado', 'ciclo_escolar').order_by('grado__numero_grado', 'nombre')
        serializer = GrupoSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Validar ciclo activo
        try:
            ciclo_activo = CicloEscolar.objects.get(activo=True)
        except CicloEscolar.DoesNotExist:
            return Response({"message": "No hay ciclo escolar activo"}, status=400)

        data = request.data.copy()
        data['ciclo_escolar'] = ciclo_activo.id
        
        # Validar grado pertenece al nivel
        grado_id = data.get('grado')
        grado = get_object_or_404(Grado, pk=grado_id)
        if grado.nivel_educativo != admin.nivel_educativo:
             return Response({"message": "El grado no pertenece a su nivel educativo"}, status=403)

        serializer = GrupoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_grupo_estudiantes(request, pk):
    """
    Lista de estudiantes de un grupo con su estatus y adeudos.
    """
    admin = request.user.admin_escolar_perfil
    grupo = get_object_or_404(Grupo, pk=pk, grado__nivel_educativo=admin.nivel_educativo)
    
    from pagos.models import Adeudo
    from django.db.models import Sum
    
    inscripciones = grupo.inscripciones.select_related('estudiante').annotate(
        adeudo_total=Sum('estudiante__adeudo__monto_total', filter=Q(estudiante__adeudo__estatus='pendiente'))
    )
    
    data = []
    for insc in inscripciones:
        est = insc.estudiante
        data.append({
            "id": est.pk,
            "matricula": est.matricula,
            "nombre_completo": f"{est.nombre} {est.apellido_paterno} {est.apellido_materno}",
            "estatus": insc.estatus,
            "adeudo_total": float(insc.adeudo_total or 0)
        })
    
    return Response(data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdministradorEscolar])
def admin_grupo_detail(request, pk):
    admin = request.user.admin_escolar_perfil
    grupo = get_object_or_404(Grupo, pk=pk, grado__nivel_educativo=admin.nivel_educativo)

    if request.method == 'PUT':
        serializer = GrupoSerializer(grupo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        # Verificar dependencias (alumnos inscritos, etc)
        if grupo.inscripciones.exists() or grupo.asignaciones_maestro.exists():
             return Response({"message": "No se puede eliminar: tiene alumnos o maestros asignados"}, status=400)
        
        grupo.delete()
        return Response({"message": "Grupo eliminado"})

@api_view(['GET'])
@permission_classes([IsAdministradorEscolar])
def admin_grados_list(request):
    """Listar grados del nivel educativo del admin."""
    admin = request.user.admin_escolar_perfil
    grados = Grado.objects.filter(nivel_educativo=admin.nivel_educativo).order_by('numero_grado')
    data = [{"id": g.id, "nombre": g.nombre, "orden": g.numero_grado} for g in grados]
    return Response(data)
