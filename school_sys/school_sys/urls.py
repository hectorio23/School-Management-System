"""
    Este url empieza aqui -> https://domain/
    puerto 443 por defecto
"""
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as http_status

from users.views import (
    EmailTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetVerifyView,
    PasswordResetConfirmView,
    admin_reporte_financiero_completo
)

# from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from . import views

from users.serializers import VerifyMFATokenView, EmailTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/token/logout/
    Blacklists the refresh token, effectively logging out the user.
    Body: { "refresh": "<refresh_token>" }
    """
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=http_status.HTTP_400_BAD_REQUEST
            )
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Sesión cerrada correctamente."}, status=http_status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "Token inválido o ya fue revocado."},
            status=http_status.HTTP_400_BAD_REQUEST
        )


urlpatterns = [
    path("", views.index),
    path('admin/', admin.site.urls),

    path("students/", include("estudiantes.urls")),
    path("academico/", include("academico.urls")),
    path('biblioteca/', include('biblioteca.urls')),
    path("api/admin/", include("users.urls")),
    path("api/admission/", include("admissions.urls")),
    path("api/comedor/", include("comedor.urls")),
    path("api/token/", EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("api/token/logout/", logout_view, name='token_logout'),

    path("api/token/mfa-verify/", VerifyMFATokenView, name="mfa_verify"),
    
    # Password Reset
    path("api/auth/password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("api/auth/password-reset/verify/", PasswordResetVerifyView.as_view(), name="password_reset_verify"),
    path("api/auth/password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("api/admin/reporte-directo/", admin_reporte_financiero_completo, name="admin_reporte_directo"),
]