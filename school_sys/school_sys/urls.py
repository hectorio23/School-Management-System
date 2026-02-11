"""
    Este url empieza aqui -> https://domain/
    puerto 443 por defecto
"""
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    EmailTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetVerifyView,
    PasswordResetConfirmView
)

# from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from . import views

from users.serializers import VerifyMFATokenView



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

    path("api/token/mfa-verify/", VerifyMFATokenView, name="mfa_verify"),
    
    # Password Reset
    path("api/auth/password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("api/auth/password-reset/verify/", PasswordResetVerifyView.as_view(), name="password_reset_verify"),
    path("api/auth/password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]