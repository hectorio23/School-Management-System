"""
    Este url empieza aqui -> https://domain/students
"""
from django.urls import path, include
from . import views
from rest_framework import routers
from academico import views as views_academico

# Use a router so POST to /students/ hits the StudentViewSet
router = routers.DefaultRouter()


urlpatterns = [
    # Information
    path("info/", views.estudiante_info_view, name="estudiante_info"),
    path("dashboard/", views.dashboard, name="estudiante_dashboard"),

    # Management
    path("tutores/", views.tutores_update_view, name="estudiante_tutores_update"),
    path("estudio-socioeconomico/", views.create_estudio_socioeconomico_view, name="estudiante_socioeconomico_create"),
    
    # Documents
    path("descargar-carta-reinscripcion/", views.download_carta_reinscripcion, name="estudiante_reinscripcion"),
    path("descargar-carta-baja/", views.download_carta_baja, name="estudiante_baja"),
    
    # Financial
    path("pagos/historial/", views.student_payments_history, name="estudiante_pagos_historial"),
    path("pagos/simular/", views.student_payment_simulator, name="estudiante_pagos_simular"),
    
    # Academic (Consolidated)
    path("calificaciones/", views_academico.estudiante_historial_view, name="estudiante_calificaciones"),

    path("api-auth/", include("rest_framework.urls")),
]