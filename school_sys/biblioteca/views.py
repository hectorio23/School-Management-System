from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import Libro, UsuarioBiblioteca, Prestamo, Multa
from .serializers import (
    LibroSerializer, UsuarioBibliotecaSerializer, 
    PrestamoSerializer, MultaSerializer
)
from .permissions import IsBibliotecario

# --- LIBROS ---

@api_view(['GET', 'POST'])
@permission_classes([IsBibliotecario])
def libro_list_create_view(request):
    """
    GET: Listar todos los libros.
    POST: Crear un nuevo libro.
    """
    if request.method == 'GET':
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsBibliotecario])
def libro_detail_view(request, pk):
    """
    GET, PUT, DELETE para un libro específico.
    """
    libro = get_object_or_404(Libro, pk=pk)
    
    if request.method == 'GET':
        serializer = LibroSerializer(libro)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        libro.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# --- PRESTAMOS ---

@api_view(['POST'])
@permission_classes([IsBibliotecario])
def realizar_prestamo_view(request):
    """
    Crea un nuevo préstamo verificando multas y disponibilidad.
    """
    libro_id = request.data.get('libro')
    usuario_id = request.data.get('usuario')
    dias_prestamo = int(request.data.get('dias', 7))
    
    libro = get_object_or_404(Libro, pk=libro_id)
    usuario = get_object_or_404(UsuarioBiblioteca, pk=usuario_id)
    
    # 1. Verificar multas pendientes
    multas_pendientes = Multa.objects.filter(prestamo__usuario=usuario, estado='pendiente').exists()
    if multas_pendientes:
        return Response(
            {"status": "error", "message": "El usuario tiene multas pendientes y no puede realizar préstamos."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 2. Verificar disponibilidad de ejemplares
    if libro.ejemplares_disponibles <= 0:
        return Response(
            {"status": "error", "message": "No hay ejemplares disponibles para este libro."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 3. Realizar préstamo
    with transaction.atomic():
        fecha_devolucion = timezone.now().date() + timezone.timedelta(days=dias_prestamo)
        prestamo = Prestamo.objects.create(
            libro=libro,
            usuario=usuario,
            fecha_de_devolucion=fecha_devolucion
        )
        
        # Actualizar stock
        libro.numero_de_ejemplares_prestados += 1
        libro.save()
        
    serializer = PrestamoSerializer(prestamo)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsBibliotecario])
def devolver_libro_view(request, pk):
    """
    Registra la devolución de un libro.
    """
    prestamo = get_object_or_404(Prestamo, pk=pk, estado='activo')
    
    with transaction.atomic():
        prestamo.estado = 'devuelto'
        prestamo.fecha_real_devolucion = timezone.now().date()
        prestamo.save()
        
        # Devolver stock
        libro = prestamo.libro
        libro.numero_de_ejemplares_prestados -= 1
        libro.save()
        
    return Response({"status": "success", "message": "Libro devuelto correctamente."}, status=status.HTTP_200_OK)

# --- MULTAS ---

@api_view(['GET'])
@permission_classes([IsBibliotecario])
def multas_list_view(request):
    """
    Listar multas. Se puede filtrar por estado.
    """
    estado = request.query_params.get('estado')
    multas = Multa.objects.all()
    if estado:
        multas = multas.filter(estado=estado)
        
    serializer = MultaSerializer(multas, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsBibliotecario])
def pagar_multa_view(request, pk):
    """
    Marca una multa como pagada.
    """
    multa = get_object_or_404(Multa, pk=pk, estado='pendiente')
    multa.estado = 'pagada'
    multa.fecha_de_pago = timezone.now().date()
    multa.save()
    
    return Response({"status": "success", "message": "Multa pagada correctamente."}, status=status.HTTP_200_OK)

# --- USUARIOS DE BIBLIOTECA ---

@api_view(['GET', 'POST'])
@permission_classes([IsBibliotecario])
def usuario_biblioteca_list_create_view(request):

    if request.method == 'GET':
        usuarios = UsuarioBiblioteca.objects.all()
        serializer = UsuarioBibliotecaSerializer(usuarios, many=True)

        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = UsuarioBibliotecaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
