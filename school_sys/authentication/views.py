from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAuthenticatedWithValidToken
from rest_framework import status, permissions
from rest_framework.response import Response
from estudiantes.models import Estudiante
from .utils import generate_tokens_for_student


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Endpoint de login único
    Autentica, genera token y retorna info de redirección según rol
    de la siguiente manera:

    POST /api/auth/login/
    Body: {
        "username": "adancito@example.com",
        "password": "password123"
    }
    
    Response: {
        "success": true,
        "access": "eyJ...",
        "refresh": "eyJ...",
        "expires_at": "2026-01-09T20:00:00Z",
        "user": {
            "id": 1,
            "username": "adancito",
            "email": "adancito@example.com",
            "role": "student"
        },
        "redirect": {
            "dashboard_url": "/estudiante/dashboard",
            "allowed_routes": [...]
        }
    }
    """
    email = request.data.get('email') # Por el momento recibirá un email
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Buscar por email
        estudiante = Estudiante.objects.get(email=email)
        
        # Verificar contraseña
        if estudiante.check_password(password):
            tokens = generate_tokens_for_student(
                estudiante, 
                request=request,
                token_duration_minutes=60 # en minutos, mas adelante este valor lo tomara de una env
            )
            return Response({
                'success': True,
                'username': estudiante.nombre,
                **tokens
            }, status=status.HTTP_202_ACCEPTED)
        else:
            raise Estudiante.DoesNotExist
            
    except Estudiante.DoesNotExist:
        return Response(
            {'success': False, 'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticatedWithValidToken])
def logout_view(request):
    """
    Cierra sesión invalidando el token actual
    
    POST /api/auth/logout/
    Headers: Authorization: Bearer <token>
    """
    if hasattr(request, 'token_record'):
        request.token_record.invalidate()
        return Response({
            'success': True,
            'message': 'Sesión cerrada correctamente'
        })
    
    return Response(
        {'error': 'Token no encontrado'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticatedWithValidToken])
def logout_all_view(request):
    """
    Cierra TODAS las sesiones del usuario
    
    POST /api/auth/logout-all/
    Headers: Authorization: Bearer <token>
    """
    invalidate_all_tokens(request.user.estudiante)
    return Response({
        'success': True,
        'message': 'Todas las sesiones cerradas'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticatedWithValidToken])
def verify_token_view(request):
    """
    Verifica si el token es válido y retorna info del usuario
    Útil para mantener sesión en frontend
    
    GET /api/auth/verify/
    Headers: Authorization: Bearer <token>
    """
    estudiante = request.user.estudiante
    
    return Response({
        'valid': True,
        'user': {
            'id': estudiante.id,
            'username': estudiante.user.username,
            'email': estudiante.email,
            'role': estudiante.role,
        },
        'token_info': {
            'expires_at': request.token_record.expires_at.isoformat(),
            'created_at': request.token_record.created_at.isoformat(),
        }
    })