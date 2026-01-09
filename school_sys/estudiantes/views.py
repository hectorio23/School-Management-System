from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, status
from .serializer import SerializerStudents
from rest_framework.response import Response
from django.shortcuts import render
from datetime import timedelta
from .models import Student
import hashlib
# from rest_framework_simplejwt.views import RefreshToker


# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [permissions.AllowAny] # Change it to permissions.IsAuthenticated for production
    serializer_class = SerializerStudents


def get_tokens_for_student(student, token_duration_minutes=None):
    """
    Genera tokens JWT para un estudiante.
    token_duration_minutes: duración personalizada del token en minutos
    """
    refresh = RefreshToken.for_user(student)
    
    # Si se especifica duración personalizada, ajustar el access token
    if token_duration_minutes:
        refresh.access_token.set_exp(lifetime=timedelta(minutes=token_duration_minutes))
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_student(request):
    """
    Endpoint de autenticación para estudiantes.
    Recibe username y password, genera hash SHA256 de "username@password"
    y lo compara con key_digest en la BD.
    Retorna tokens JWT con duración configurable.
    """
    if request.method == 'POST':
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        token_duration = request.data.get('token_duration', None)  # en minutos
        
        if not username or not password:
            return Response(
                {
                    'success': False,
                    'error': 'Username and password are required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generar hash SHA256 de "username@password"
        credentials = f"{username}@{password}"
        hash_generated = hashlib.sha256(credentials.encode()).hexdigest()
        
        # Buscar estudiante por key_digest
        try:
            student = Student.objects.get(key_digest=hash_generated)
            
            # Generar tokens JWT
            tokens = get_tokens_for_student(student, token_duration)
            
            serializer = SerializerStudents(student)
            
            response = Response(
                {
                    'success': True,
                    'message': 'Authentication successful',
                    'student': serializer.data,
                    'access_token': tokens['access'],
                    'refresh_token': tokens['refresh'],
                },
                status=status.HTTP_200_OK
            )
            
            # Establecer cookie HttpOnly con el access token
            max_age = token_duration * 60 if token_duration else 3600  # en segundos
            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                max_age=max_age,
                httponly=True,
                secure=False,  # Cambiar a True en producción con HTTPS
                samesite='Lax'
            )
            
            return response
            
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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_token(request):
    """
    Verifica si un token JWT es válido.
    """
    from rest_framework_simplejwt.tokens import AccessToken
    from rest_framework_simplejwt.exceptions import TokenError
    
    token = request.COOKIES.get('access_token') or request.data.get('token')
    
    if not token:
        return Response(
            {'valid': False, 'error': 'No token provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Validar token
        AccessToken(token)
        # Obtener el user_id del token
        token_obj = AccessToken(token)
        user_id = token_obj['user_id']
        
        # Obtener datos del estudiante
        student = Student.objects.get(id=user_id)
        serializer = SerializerStudents(student)
        
        return Response(
            {
                'valid': True,
                'student': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except TokenError:
        return Response(
            {'valid': False, 'error': 'Invalid or expired token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Student.DoesNotExist:
        return Response(
            {'valid': False, 'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_student(request):
    """
    Cierra la sesión eliminando la cookie.
    """
    response = Response(
        {'success': True, 'message': 'Logged out successfully'},
        status=status.HTTP_200_OK
    )
    response.delete_cookie('access_token')
    return response