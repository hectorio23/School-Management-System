from .serializer import SerializerStudents
from .models import Student
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import hashlib

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [permissions.AllowAny] # Change it to permissions.IsAuthenticated for production
    serializer_class = SerializerStudents


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_student(request):
    """
    Endpoint de autenticación para estudiantes.
    Recibe un hash SHA256 de "username@password" y lo compara con key_digest en la BD.
    """
    if request.method == 'POST':
        hash_received = request.data.get('hash', '').strip()
        
        if not hash_received:
            return Response(
                {'error': 'Hash is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar estudiante por key_digest
        try:
            student = Student.objects.get(key_digest=hash_received)
            serializer = SerializerStudents(student)
            return Response(
                {
                    'success': True,
                    'message': 'Authentication successful',
                    'student': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Student.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid credentials'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(
        {'error': 'Method not allowed'},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
