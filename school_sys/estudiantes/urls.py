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
    
    # Endpoints para descarga de documentos
    path("descargar-carta-reinscripcion/", views.download_carta_reinscripcion, name="descargar_carta_reinscripcion"),
    path("descargar-carta-baja/", views.download_carta_baja, name="descargar_carta_baja"),
    
    # Endpoints Financieros (RF-CTA-02, RF-CAL-04, RF-PAG-01)
    path("pagos/historial/", views.student_payments_history, name="student_payments_history"),
    path("pagos/simular/", views.student_payment_simulator, name="student_payment_simulator"),
    # path("pagos/subir-comprobante/", views.student_upload_receipt, name="student_upload_receipt"),
    
    path("api-auth/", include("rest_framework.urls")),
    # Router al final para capturar las demás rutas
    path("", include(router.urls)),
]