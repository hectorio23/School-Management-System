from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Estudiante
from .serializer import SerializerStudent
from authentication.permissions import IsAuthenticatedWithValidToken

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = SerializerStudent
    
    def get_permissions(self):
        """
        Permisos dinámicos según la acción
        """
        if self.action == 'create':
            # Permitir registro sin autenticación
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Requiere autenticación y ser dueño
            permission_classes = [IsAuthenticatedWithValidToken, IsStudentOwner]
        elif self.action == 'list':
            # Solo admins pueden listar todos
            permission_classes = [IsAuthenticatedWithValidToken, CanModifyRecords]
        else:
            permission_classes = [IsAuthenticatedWithValidToken]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Endpoint de login con registro de token"""
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            student = Estudiante.objects.get(email=email)
            if student.check_password(password):  # Asume método check_password
                tokens = get_tokens_for_student(
                    student, 
                    token_duration_minutes=60,
                    request=request
                )
                return Response({
                    'tokens': tokens,
                    'student': SerializerStudent(student).data
                })
        except Estudiante.DoesNotExist:
            pass
        
        return Response(
            {'error': 'Credenciales inválidas'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedWithValidToken])
    def logout(self, request):
        """Logout que invalida el token actual"""
        if hasattr(request, 'token_record'):
            request.token_record.invalidate()
            return Response({'message': 'Sesión cerrada correctamente'})
        return Response(
            {'error': 'Token no encontrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticatedWithValidToken])
    def logout_all(self, request):
        """Cierra todas las sesiones del usuario"""
        invalidate_all_student_tokens(request.user.estudiante)
        return Response({'message': 'Todas las sesiones cerradas'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedWithValidToken])
    def active_sessions(self, request):
        """Lista las sesiones activas del usuario"""
        tokens = TokenRegistry.objects.filter(
            student=request.user.estudiante,
            is_active=True
        ).order_by('-created_at')
        
        sessions = [{
            'created_at': t.created_at,
            'last_used': t.last_used_at,
            'ip_address': t.ip_address,
            'expires_at': t.expires_at,
            'is_current': t.jti == request.token_record.jti if hasattr(request, 'token_record') else False
        } for t in tokens]
        
        return Response({'sessions': sessions})


# Task para limpiar tokens expirados (celery/cron)
def cleanup_expired_tokens():
    """Tarea periódica para limpiar tokens expirados"""
    expired_count = TokenRegistry.objects.filter(
        is_active=True,
        expires_at__lt=timezone.now()
    ).update(is_active=False)
    
    # Opcional: eliminar tokens antiguos
    old_tokens = TokenRegistry.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=30)
    )
    deleted_count = old_tokens.count()
    old_tokens.delete()
    
    return f"Expirados: {expired_count}, Eliminados: {deleted_count}"