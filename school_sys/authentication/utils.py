from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import TokenRegistry
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import uuid

def get_client_ip(request):
    """Obtiene IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def generate_tokens_for_student(student, request=None, token_duration_minutes=60):
    """Genera tokens JWT sin User de Django"""
    from rest_framework_simplejwt.tokens import RefreshToken
    from datetime import timedelta
    from django.utils import timezone
    from django.conf import settings
    import uuid
    
    # Crear pseudo-user para JWT
    class PseudoUser:
        def __init__(self, student):
            self.pk = student.matricula
            self.id = student.matricula
            self.is_active = True
    
    pseudo_user = PseudoUser(student)
    refresh = RefreshToken.for_user(pseudo_user)
    
    # Generar JTI único
    jti = str(uuid.uuid4())
    refresh['jti'] = jti
    refresh.access_token['jti'] = jti
    
    # Embeber rol y datos en el token
    refresh['role'] = student.role
    refresh['matricula'] = student.matricula
    refresh['email'] = student.email
    
    refresh.access_token['role'] = student.role
    refresh.access_token['matricula'] = student.matricula
    refresh.access_token['email'] = student.email
    
    # Configurar expiración
    refresh.access_token.set_exp(lifetime=timedelta(minutes=token_duration_minutes))
    expires_at = timezone.now() + timedelta(minutes=token_duration_minutes)
    
    # Obtener metadata
    ip_address = get_client_ip(request) if request else None
    user_agent = request.META.get('HTTP_USER_AGENT', '') if request else ''
    
    # CAMBIO: Guardar con estudiante directamente
    TokenRegistry.objects.create(
        estudiante=student,  # ← Era 'user=student.user'
        jti=jti,
        access_token=str(refresh.access_token),
        refresh_token=str(refresh),
        issued_role=student.role,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    # Determinar rutas según rol
    if student.is_admin:
        dashboard_url = '/admin/dashboard'
        allowed_routes = [
            '/admin/dashboard',
            '/admin/students',
            '/admin/records',
            '/admin/reports',
            '/admin/settings'
        ]
    else:
        dashboard_url = '/student/dashboard'
        allowed_routes = [
            '/student/dashboard',
            '/student/profile',
            '/student/grades',
            '/student/schedule'
        ]
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'expires_at': expires_at.isoformat(),
        'user': {
            'matricula': student.matricula,
            'nombre': student.nombre,
            'apellido_paterno': student.apellido_paterno,
            'email': student.email,
            'role': student.role,
        },
        'redirect': {
            'dashboard_url': dashboard_url,
            'allowed_routes': allowed_routes
        }
    }

def invalidate_all_tokens(student):
    """Invalida todos los tokens de un estudiante"""
    TokenRegistry.objects.filter(
        estudiante=student,
        is_active=True
    ).update(is_active=False)