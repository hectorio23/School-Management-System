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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students/tutores', views.AdminTutorViewSet, basename='admin-tutores')
router.register(r'pagos/adeudos', views.AdminAdeudoViewSet, basename='admin-adeudos')
router.register(r'pagos', views.AdminPagoViewSet, basename='admin-pagos')
router.register(r'students/evaluaciones', views.AdminEvaluacionViewSet, basename='admin-evaluaciones')

urlpatterns = [
    # estudiantes 
    path('students/', views.admin_student_list, name='admin_student_list'),
    path('students/<int:matricula>/', views.admin_student_detail, name='admin_student_detail'),
    path('students/create/', views.AdminStudentOpsView.as_view(), name='admin_student_create'), 
    path('students/<int:matricula>/update/', views.AdminStudentDetailOpsView.as_view(), name='admin_student_update'), 

    # -- Endpoints basados en ViewSets --
    path('', include(router.urls)),
]
