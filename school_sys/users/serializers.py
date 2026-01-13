from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.response import Response

from .utils import send_mfa_code, verify_mfa_code
User = get_user_model()

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

        if not login_input:
            raise serializers.ValidationError("Must provide 'username' or 'email'.")

        # Buscar usuario
        user = User.objects.filter(
            Q(username=login_input) | Q(email=login_input)
        ).first()

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        # AQUI VIENE EL FIX CRÍTICO:
        # Garantizar que SimpleJWT SIEMPRE reciba username/email en attrs["username"]
        attrs["username"] = user.email  # aunque el usuario haya ingresado username

        if "email" in attrs:
            del attrs["email"]

        # Llamar a SimpleJWT (validación de password)
        data = super().validate(attrs)

        # Evaluar rol después del password correcto
        print(user)
        if user.role in ("administrador", "admin", "Admin", "ADMIN", "Administrador"):
            send_mfa_code(user)

            return {
                "mfa_required": True,
                "username": user.username,
                "detail": "MFA code sent.",
                "expired_at":   timezone.now() + timedelta(minutes=2)
            }

        # Flujo normal
        data["mfa_required"] = False
        return data