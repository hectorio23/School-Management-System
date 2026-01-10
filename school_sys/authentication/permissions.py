from estudiantes.models import Estudiante
from rest_framework import permissions
from .models import TokenRegistry
from django.conf import settings
import jwt

# authentication/permissions.py
class IsAuthenticatedWithValidToken(permissions.BasePermission):
    """Valida token registrado y rol"""
    message = "[-] Token inválido o rol no coincide"
    
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decodificar token
            decoded = jwt.decode(
                token, 
                settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[settings.SIMPLE_JWT['ALGORITHM']]
            )
            
            jti = decoded.get('jti')
            token_role = decoded.get('role')
            matricula = decoded.get('matricula')
            
            # Buscar estudiante
            try:
                estudiante = Estudiante.objects.get(matricula=matricula)
            except Estudiante.DoesNotExist:
                return False
            
            # Buscar token en registro
            token_record = TokenRegistry.objects.filter(
                jti=jti,
                is_active=True,
                estudiante=estudiante  # ← Ya no es 'user'
            ).first()
            
            if not token_record:
                return False
            
            # Validar no expirado
            if token_record.is_expired():
                token_record.invalidate()
                return False
            
            # Validar rol coincide
            if token_record.issued_role != token_role:
                token_record.invalidate()
                return False
            
            # Validar rol actual coincide
            if estudiante.role != token_role:
                token_record.invalidate()
                return False
            
            # Actualizar último uso
            token_record.last_used_at = timezone.now()
            token_record.save(update_fields=['last_used_at'])
            
            # Guardar en request
            request.token_record = token_record
            request.estudiante = estudiante
            request.user_role = token_role
            
            return True
            
        except (jwt.InvalidTokenError, AttributeError):
            return False