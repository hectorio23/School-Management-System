"""
**************** ENDPOINTS DEL PROYECTO ****************

NOTA: todos los datos excepto email van en MAYUSCULAS para evitar inconsistencias a la hora de validar

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
POST api/admin/students/<matricula>/baja/ -> procesar baja con calculo adeudos

--- ADMIN TUTORES ---
GET  api/admin/students/tutores/         -> lista tutores (150/pag)
POST api/admin/students/tutores/         -> crear tutor
GET  api/admin/students/tutores/<id>/    -> detalle tutor
PUT  api/admin/students/tutores/<id>/    -> update tutor
DELETE api/admin/students/tutores/<id>/  -> eliminar tutor

--- ADMIN ESTRATOS ---
GET  api/admin/estratos/                 -> lista todos los estratos
POST api/admin/estratos/                 -> crear estrato (con color, rangos ingreso)
GET  api/admin/estratos/<id>/            -> detalle estrato
PUT  api/admin/estratos/<id>/            -> update estrato
DELETE api/admin/estratos/<id>/          -> desactiva estrato (no elimina)

--- ADMIN EVALUACIONES SOCIOECONOMICAS ---
GET  api/admin/evaluaciones/             -> lista pendientes (o todas con ?pendientes=false)
PUT  api/admin/evaluaciones/<id>/aprobar/ -> aprobar/rechazar con comentarios comision

--- ADMIN ADEUDOS ---
POST api/admin/adeudos/generar-mensual/  -> genera adeudos del mes para todos los estudiantes activos
POST api/admin/adeudos/aplicar-recargos/ -> aplica 10% + $125 a vencidos
POST api/admin/adeudos/<id>/exentar/     -> quita recargo con justificacion
GET  api/admin/adeudos/vencidos/         -> lista adeudos vencidos

--- ADMIN PAGOS ---
GET  api/admin/pagos/            -> lista pagos (50/pag)
POST api/admin/pagos/            -> crear pago
GET  api/admin/pagos/<id>/       -> detalle pago
PUT  api/admin/pagos/<id>/       -> update pago
DELETE api/admin/pagos/<id>/     -> NO SE PUEDE, bloqueado

--- ADMIN CONFIGURACION ---
GET  api/admin/configuracion-pago/   -> ver config actual (dias ordinarios, recargos)
PUT  api/admin/configuracion-pago/   -> actualizar config

--- ADMIN COMEDOR ---
GET  api/admin/comedor/menus/            -> lista menus semanales activos
POST api/admin/comedor/menus/            -> subir PDF menu semanal
GET  api/admin/comedor/asistencia/       -> reporte asistencia (?desde=&hasta=)
GET  api/admin/comedor/alergias/         -> alumnos con alergias alimentarias

--- ADMIN REPORTES ---
GET  api/admin/reportes/ingresos-estrato/  -> ingresos agrupados por estrato
GET  api/admin/reportes/recaudacion/       -> ordinaria vs recargos

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
    # estudiantes
    path('students/', views.admin_student_list, name='admin_student_list'),
    path('students/<int:pk>/', views.admin_student_detail, name='admin_student_detail'),
    path('students/<int:pk>/baja/', views.admin_estudiante_baja, name='admin_estudiante_baja'),

    # tutores
    path('students/tutores/', views.admin_tutor_list, name='admin_tutor_list'),
    path('students/tutores/<int:pk>/', views.admin_tutor_detail, name='admin_tutor_detail'),

    # estratos
    path('estratos/', views.admin_estrato_list, name='admin_estrato_list'),
    path('estratos/<int:pk>/', views.admin_estrato_detail, name='admin_estrato_detail'),

    # evaluaciones
    path('evaluaciones/', views.admin_evaluacion_list, name='admin_evaluacion_list'),
    path('evaluaciones/<int:pk>/aprobar/', views.admin_evaluacion_aprobar, name='admin_evaluacion_aprobar'),

    # adeudos
    path('adeudos/generar-mensual/', views.admin_generar_adeudos_mensuales, name='admin_generar_adeudos'),
    path('adeudos/aplicar-recargos/', views.admin_aplicar_recargos, name='admin_aplicar_recargos'),
    path('adeudos/<int:pk>/exentar/', views.admin_exentar_recargo, name='admin_exentar_recargo'),
    path('adeudos/vencidos/', views.admin_adeudos_vencidos, name='admin_adeudos_vencidos'),

    # pagos
    path('pagos/', views.admin_pago_list, name='admin_pago_list'),
    path('pagos/<int:pk>/', views.admin_pago_detail, name='admin_pago_detail'),

    # configuracion
    path('configuracion-pago/', views.admin_configuracion_pago, name='admin_configuracion_pago'),

    # comedor
    path('comedor/menus/', views.admin_menu_semanal_list, name='admin_menu_semanal_list'),
    path('comedor/asistencia/', views.admin_comedor_asistencia, name='admin_comedor_asistencia'),
    path('comedor/alergias/', views.admin_alumnos_alergias, name='admin_alumnos_alergias'),

    # reportes
    path('reportes/ingresos-estrato/', views.admin_reporte_ingresos_estrato, name='admin_reporte_ingresos_estrato'),
    path('reportes/recaudacion/', views.admin_reporte_recaudacion, name='admin_reporte_recaudacion'),
]
