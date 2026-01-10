"""
    Este url empieza aqui -> https://domain/
    puerto 443 por defecto
"""
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from estudiantes.views import StudentViewSet
from django.conf.urls.static import static
from django.urls import path, include

from authentication.views import * 
# Endpoints de authentication.views
#    login_view -> Inicio de sesion <Creación de una nueva sesion>, 
#    logout_view -> Cerrar sesión actual, 
#    logout_all_view -> Cerrar todas las sesiones activas de un usuario 

from django.contrib import admin
from . import views


router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path("", views.index),
    path('admin/', admin.site.urls),
    path("students/", include("estudiantes.urls")),
    
    # Resource endpoints
    path('api/', include(router.urls)),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/logout-all/', logout_all_view, name='logout-all'),
    path('api/auth/verify/', verify_token_view, name='verify-token'),
    
]