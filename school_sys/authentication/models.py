from django.contrib.auth.models import User
from estudiantes.models import Estudiante, UserRole
from django.utils import timezone
from django.db import models

# models.py
class TokenRegistry(models.Model):
    """Registro de tokens activos"""
    # CAMBIO: Apunta directamente a Estudiante, no a User
    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name='tokens'
    )
    
    jti = models.CharField(max_length=255, unique=True, db_index=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    issued_role = models.CharField(max_length=20, choices=UserRole.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'token_registry'
        indexes = [
            models.Index(fields=['jti']),
            models.Index(fields=['estudiante', 'is_active']),
        ]
    
    def invalidate(self):
        self.is_active = False
        self.save()
    
    def is_expired(self):
        return timezone.now() > self.expires_at