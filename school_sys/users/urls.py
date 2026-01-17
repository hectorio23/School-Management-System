"""
**************** ENDPOINTS DEL PROYECTO ****************

--- AUTH ---
POST api/token/                     -> login, obtiene JWT
POST auth/token/refresh/            -> refrescar token
POST api/token/mfa-verify/          -> verificar MFA (solo admins)

--- ADMIN ESTUDIANTES (api/admin/) ---
GET  api/admin/students/                 -> lista estudiantes (60/pag)
POST api/admin/students/                 -> crear estudiante (crea User + Estudiante)
GET  api/admin/students/<matricula>/     -> detalle estudiante
PUT  api/admin/students/<matricula>/     -> actualizar estudiante
DELETE api/admin/students/<matricula>/   -> soft delete (estado = Baja)

--- ADMIN TUTORES ---
GET  api/admin/students/tutores/         -> lista tutores (150/pag)
POST api/admin/students/tutores/         -> crear tutor
GET  api/admin/students/tutores/<id>/    -> detalle tutor
PUT  api/admin/students/tutores/<id>/    -> update tutor
DELETE api/admin/students/tutores/<id>/  -> eliminar tutor

--- ADMIN PAGOS ---
GET  api/admin/pagos/            -> lista pagos (50/pag)
POST api/admin/pagos/            -> crear pago
GET  api/admin/pagos/<id>/       -> detalle pago
PUT  api/admin/pagos/<id>/       -> update pago
DELETE api/admin/pagos/<id>/     -> NO SE PUEDE, bloqueado

--- TODO: ADMIN ESTRATOS --- 

--- ESTUDIANTES (students/) ---
GET  students/info/                      -> info personal del estudiante logueado
GET  students/dashboard/                 -> dashboard
POST students/tutores/                   -> actualizar tutores
POST students/estudio-socioeconomico/    -> crear estudio socioeconomico

--- DJANGO ADMIN ---
admin/   -> panel admin django

"""

from django.urls import path
from . import views

urlpatterns = [
    # Endpoint de administrador para listar estudiantes (paginado 60/página)
    # Retorna info esencial: matricula, apellidos, grado, grupo, etc.
    path('students/', views.admin_student_list, name='admin_student_list'),
    path('students/<int:pk>/', views.admin_student_detail, name='admin_student_detail'),

    # Retorna información sobre los tutores 
    path('students/tutores/', views.admin_tutor_list, name='admin_tutor_list'),
    path('students/tutores/<int:pk>/', views.admin_tutor_detail, name='admin_tutor_detail'),

    # PAgos, Solo lectura
    path('pagos/', views.admin_pago_list, name='admin_pago_list'),
    path('pagos/<int:pk>/', views.admin_pago_detail, name='admin_pago_detail'),
]
