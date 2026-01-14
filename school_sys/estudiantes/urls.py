"""
    Este url empieza aqui -> https://domain/students
"""
from django.urls import path, include
from . import views
from rest_framework import routers

# Use a router so POST to /students/ hits the StudentViewSet
router = routers.DefaultRouter()

urlpatterns = [
    # Endpoint para información personal del estudiante autenticado
    path("info/", views.estudiante_info_view, name="estudiante_info"),
    path("dashboard/", views.dashboard, name="estudiante_info"),

    # Endpoint para actualizar tutores del estudiante
    path("tutores/", views.tutores_update_view, name="tutores_update"),

    # Endpoint para crear un nuevo estudio socieconomico
    path("estudio-socioeconomico/", views.create_estudio_socioeconomico_view, name="estudio_socioeconomico"),
    
    path("api-auth/", include("rest_framework.urls")),
    # Router al final para capturar las demás rutas
    path("", include(router.urls)),
]