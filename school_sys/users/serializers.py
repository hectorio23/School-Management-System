from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import timedelta
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.response import Response
import os

from .utils import send_mfa_code, verify_mfa_code
from .models import LoginAttempt

User = get_user_model()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['POST'])
@permission_classes([AllowAny])
def VerifyMFATokenView(request):
    email = request.data.get("email")
    code = request.data.get("code")

    if not email or not code:
        return Response({"detail": "email and code are required"}, status=400)

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"detail": "Invalid user"}, status=400)

    # Validación MFA
    if not verify_mfa_code(user, code):
        return Response({"detail": "Invalid or expired code"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": "admin",
        },
        status=200,
    )

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "username"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = serializers.CharField(required=False)
        self.fields["email"] = serializers.CharField(required=False)

    def validate(self, attrs):
        login_input = attrs.get("username") or attrs.get("email")
        request = self.context.get('request')
        ip_address = get_client_ip(request) if request else '0.0.0.0'

        if not login_input:
            raise serializers.ValidationError("Must provide 'username' or 'email'.")

        # 1. Verificar Rate Limiting (Intentos Fallidos)
        max_attempts = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
        window_minutes = int(os.getenv('LOGIN_ATTEMPTS_WINDOW_MINUTES', 15))
        lockout_minutes = int(os.getenv('LOGIN_LOCKOUT_MINUTES', 30))
        
        time_threshold = timezone.now() - timedelta(minutes=window_minutes)
        
        failed_attempts = LoginAttempt.objects.filter(
            Q(email=login_input) | Q(ip_address=ip_address),
            timestamp__gte=time_threshold,
            was_successful=False
        ).count()

        if failed_attempts >= max_attempts:
            raise serializers.ValidationError(
                f"Demasiados intentos fallidos. Intente de nuevo en {lockout_minutes} minutos."
            )

        # Buscar usuario
        user = User.objects.filter(
            Q(username=login_input) | Q(email=login_input)
        ).first()

        # Si el usuario existe, aseguramos que el campo username tenga el email (para simplejwt)
        if user:
            attrs["username"] = user.email
            if "email" in attrs:
                del attrs["email"]

        # 2. Intentar autenticación (Llamar a SimpleJWT)
        try:
            data = super().validate(attrs)
        except Exception as e:
            # Registrar intento fallido
            LoginAttempt.objects.create(
                email=login_input,
                ip_address=ip_address,
                was_successful=False
            )
            # Si no existe el usuario, lanzamos error genérico
            if not user:
                 raise serializers.ValidationError("Credenciales inválidas.")
            raise e

        # 3. Autenticación exitosa -> Registrar intento exitoso
        LoginAttempt.objects.create(
            email=user.email,
            ip_address=ip_address,
            was_successful=True
        )

        # Configurar expiración
        data.update(
            {"expired_at": timezone.now() + timedelta(minutes=2)}
        )

        # Evaluar rol después del password correcto (MFA para administradores)
        if user.role in ("administrador", "admin", "Admin", "ADMIN", "Administrador"):
            send_mfa_code(user)

            return {
                "mfa_required": True,
                "username": user.username,
                "detail": "MFA code sent.",
                "expired_at": timezone.now() + timedelta(minutes=2)
            }

        # Bloquear aspirantes del login principal
        if user.role == 'aspirante':
            raise serializers.ValidationError("Los aspirantes deben iniciar sesión en el Portal de Aspirantes.")

        # Flujo normal
        return data