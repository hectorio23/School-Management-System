"""
**************** ENDPOINTS DEL PROYECTO ****************

NOTA: todos los datos excepto email van en MAYUSCULAS para evitar inconsistencias a la hora de validar

--- AUTH ---
POST api/token/                     -> login, obtiene JWT
POST auth/token/refresh/            -> refrescar token
POST api/token/mfa-verify/          -> verificar MFA (solo admins)

--- ADMIN ESTUDIANTES (api/admin/) ---
GET  api/admin/students/                 -> lista estudiantes (60/pag)
POST api/admin/students/create/          -> crear estudiante (crea User + Estudiante)
GET  api/admin/students/<matricula>/     -> detalle estudiante
PUT  api/admin/students/<matricula>/update/  -> actualizar estudiante
DELETE api/admin/students/<matricula>/update/  -> soft delete (estado = Baja)

--- ADMIN TUTORES ---
GET  api/admin/students/tutores/         -> lista tutores (150/pag)
POST api/admin/students/tutores/         -> crear tutor
GET  api/admin/students/tutores/<id>/    -> detalle tutor
PUT  api/admin/students/tutores/<id>/    -> update tutor
DELETE api/admin/students/tutores/<id>/  -> eliminar tutor

--- ADMIN CONCEPTOS DE PAGO ---
GET  api/admin/conceptos/                -> lista conceptos
POST api/admin/conceptos/                -> crear concepto
GET  api/admin/conceptos/<id>/           -> detalle concepto
PUT  api/admin/conceptos/<id>/           -> update concepto
DELETE api/admin/conceptos/<id>/         -> eliminar concepto
POST api/admin/conceptos/<id>/generar-adeudos/  -> generar adeudos masivos

--- ADMIN GRADOS ---
GET  api/admin/grados/                   -> lista grados
POST api/admin/grados/                   -> crear grado
GET  api/admin/grados/<id>/              -> detalle grado
PUT  api/admin/grados/<id>/              -> update grado
DELETE api/admin/grados/<id>/            -> eliminar grado

--- ADMIN GRUPOS ---
GET  api/admin/grupos/                   -> lista grupos
POST api/admin/grupos/                   -> crear grupo
GET  api/admin/grupos/<id>/              -> detalle grupo
PUT  api/admin/grupos/<id>/              -> update grupo
DELETE api/admin/grupos/<id>/            -> eliminar grupo

--- ADMIN ESTRATOS ---
GET  api/admin/estratos/                 -> lista estratos
POST api/admin/estratos/                 -> crear estrato
GET  api/admin/estratos/<id>/            -> detalle estrato
PUT  api/admin/estratos/<id>/            -> update estrato
DELETE api/admin/estratos/<id>/          -> desactivar estrato

--- ADMIN ESTADOS ---
GET  api/admin/estados/                  -> lista estados de estudiante
POST api/admin/estados/                  -> crear estado
GET  api/admin/estados/<id>/             -> detalle estado
PUT  api/admin/estados/<id>/             -> update estado
DELETE api/admin/estados/<id>/           -> eliminar estado

--- ADMIN BECAS ---
GET  api/admin/becas/                    -> lista becas
POST api/admin/becas/                    -> crear beca
GET  api/admin/becas/<id>/               -> detalle beca
PUT  api/admin/becas/<id>/               -> update beca
DELETE api/admin/becas/<id>/             -> eliminar beca
POST api/admin/becas/verificar-vigencia/ -> verificar y actualizar vigencia

--- ADMIN BECAS-ESTUDIANTES ---
GET  api/admin/becas-estudiantes/        -> lista asignaciones
POST api/admin/becas-estudiantes/        -> asignar beca
GET  api/admin/becas-estudiantes/<id>/   -> detalle asignación
PUT  api/admin/becas-estudiantes/<id>/   -> update asignación
DELETE api/admin/becas-estudiantes/<id>/ -> eliminar asignación
POST api/admin/becas-estudiantes/retirar-masivo/  -> retirar becas masivo
POST api/admin/becas-estudiantes/activar-masivo/  -> activar becas masivo

--- ADMIN ADEUDOS ---
GET  api/admin/pagos/adeudos/            -> lista adeudos
POST api/admin/pagos/adeudos/            -> crear adeudo
GET  api/admin/pagos/adeudos/<id>/       -> detalle adeudo
PUT  api/admin/pagos/adeudos/<id>/       -> update adeudo
DELETE api/admin/pagos/adeudos/<id>/     -> eliminar adeudo
GET  api/admin/pagos/adeudos/vencidos/   -> lista adeudos vencidos
POST api/admin/pagos/adeudos/recalcular/ -> recalcular recargos
POST api/admin/pagos/adeudos/<id>/exentar/  -> exentar recargo

--- ADMIN PAGOS ---
GET  api/admin/pagos/                    -> lista pagos
POST api/admin/pagos/                    -> crear pago
GET  api/admin/pagos/<id>/               -> detalle pago
PUT  api/admin/pagos/<id>/               -> update pago
DELETE api/admin/pagos/<id>/             -> BLOQUEADO

--- ADMIN EVALUACIONES ---
GET  api/admin/students/evaluaciones/    -> lista evaluaciones
GET  api/admin/students/evaluaciones/<id>/ -> detalle evaluación

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

        # --- ADMIN PANEL ---
    path('dashboard/', views.dashboard),

    # --- ESTUDIANTES ---
    path('students/', views.admin_student_list, name='admin_student_list'),
    path('students/create/', views.admin_student_create, name='admin_student_create'),
    path('students/<int:matricula>/', views.admin_student_detail, name='admin_student_detail'),
    path('students/<int:matricula>/update/', views.admin_student_update, name='admin_student_update'),

    # --- TUTORES ---
    path('students/tutores/', views.admin_tutores_list, name='admin_tutores_list'),
    path('students/tutores/<int:pk>/', views.admin_tutores_detail, name='admin_tutores_detail'),

    # --- EVALUACIONES ---
    path('students/evaluaciones/', views.admin_evaluaciones_list, name='admin_evaluaciones_list'),
    path('students/evaluaciones/<int:pk>/', views.admin_evaluaciones_detail, name='admin_evaluaciones_detail'),

    # --- CONCEPTOS DE PAGO ---
    path('conceptos/', views.admin_conceptos_list, name='admin_conceptos_list'),
    path('conceptos/<int:pk>/', views.admin_conceptos_detail, name='admin_conceptos_detail'),
    path('conceptos/<int:pk>/generar-adeudos/', views.admin_conceptos_generar_adeudos, name='admin_conceptos_generar_adeudos'),

    # --- GRADOS ---
    path('grados/', views.admin_grados_list, name='admin_grados_list'),
    path('grados/<int:pk>/', views.admin_grados_detail, name='admin_grados_detail'),

    # --- GRUPOS ---
    path('grupos/', views.admin_grupos_list, name='admin_grupos_list'),
    path('grupos/<int:pk>/', views.admin_grupos_detail, name='admin_grupos_detail'),

    # --- ESTRATOS ---
    path('estratos/', views.admin_estratos_list, name='admin_estratos_list'),
    path('estratos/<int:pk>/', views.admin_estratos_detail, name='admin_estratos_detail'),

    # --- ESTADOS ---
    path('estados/', views.admin_estados_list, name='admin_estados_list'),
    path('estados/<int:pk>/', views.admin_estados_detail, name='admin_estados_detail'),

    # --- BECAS ---
    path('becas/', views.admin_becas_list, name='admin_becas_list'),
    path('becas/verificar-vigencia/', views.admin_becas_verificar_vigencia, name='admin_becas_verificar_vigencia'),
    path('becas/<int:pk>/', views.admin_becas_detail, name='admin_becas_detail'),

    # --- BECAS-ESTUDIANTES ---
    path('becas-estudiantes/', views.admin_becas_estudiantes_list, name='admin_becas_estudiantes_list'),
    path('becas-estudiantes/retirar-masivo/', views.admin_becas_estudiantes_retirar_masivo, name='admin_becas_estudiantes_retirar_masivo'),
    path('becas-estudiantes/activar-masivo/', views.admin_becas_estudiantes_activar_masivo, name='admin_becas_estudiantes_activar_masivo'),
    path('becas-estudiantes/<int:pk>/', views.admin_becas_estudiantes_detail, name='admin_becas_estudiantes_detail'),

    # --- ADEUDOS ---
    path('pagos/adeudos/', views.admin_adeudos_list, name='admin_adeudos_list'),
    path('pagos/adeudos/vencidos/', views.admin_adeudos_vencidos, name='admin_adeudos_vencidos'),
    path('pagos/adeudos/recalcular/', views.admin_adeudos_recalcular, name='admin_adeudos_recalcular'),
    path('pagos/adeudos/<int:pk>/', views.admin_adeudos_detail, name='admin_adeudos_detail'),
    path('pagos/adeudos/<int:pk>/exentar/', views.admin_adeudos_exentar, name='admin_adeudos_exentar'),

    # --- PAGOS ---
    path('pagos/', views.admin_pagos_list, name='admin_pagos_list'),
    path('pagos/<int:pk>/', views.admin_pagos_detail, name='admin_pagos_detail'),
]
