from django.urls import path
from . import views

urlpatterns = [
    # Endpoint de administrador para listar estudiantes (paginado 60/página)
    # Retorna info esencial: matricula, apellidos, grado, grupo, etc.
    path('students/', views.admin_student_list, name='admin_student_list'),

    # Endpoint de administrador para ver detalle completo de un estudiante
    # Retorna toda la información relacionada: tutores, historial, evaluaciones, etc.
    path('students/<int:matricula>/', views.admin_student_detail, name='admin_student_detail'),
]
