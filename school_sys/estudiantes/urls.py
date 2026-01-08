from django.urls import path, include
from . import views
from rest_framework import routers

# Use a router so POST to /students/ hits the StudentViewSet
router = routers.DefaultRouter()
router.register(r"", views.StudentViewSet, basename="students")

urlpatterns = [
    # Login debe ir ANTES del router para que no sea interceptado
    path("login/", views.login_student, name="login_student"),
    path("api-auth/", include("rest_framework.urls")),
    # Router al final para capturar las demás rutas
    path("", include(router.urls)),
]