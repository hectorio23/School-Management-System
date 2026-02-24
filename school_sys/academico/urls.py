from django.urls import path
from . import views

urlpatterns = [
    # Admin Escolar
    path('api/admin-escolar/maestros/', views.admin_maestros_list_create, name='admin-maestros-list'),
    path('api/admin-escolar/maestros/<int:pk>/', views.admin_maestro_detail, name='admin-maestro-detail'),
    path('api/admin-escolar/grupos/', views.admin_grupos_list_create, name='admin-grupos-list'),
    path('api/admin-escolar/grupos/<int:pk>/', views.admin_grupo_detail, name='admin-grupo-detail'),
    path('api/admin-escolar/grupos/<int:pk>/estudiantes/', views.admin_grupo_estudiantes, name='admin-grupo-estudiantes'),
    path('api/admin-escolar/grados/', views.admin_grados_list, name='admin-grados-list'),
    path('api/admin-escolar/materias/', views.admin_materias_list_create, name='admin-materias-list'),
    path('api/admin-escolar/materias/<int:pk>/', views.admin_materia_detail, name='admin-materia-detail'),
    path('api/admin-escolar/programas/', views.admin_programas_list, name='admin-programas-list'),
    # path('api/admin-escolar/materias/<int:pk>/desactivar/', views.admin_materia_desactivar, name='admin-materia-desactivar'), # Replaced by detail DELETE
    path('api/admin-escolar/asignaciones/', views.admin_asignaciones_list_create, name='admin-asignaciones-list'),
    path('api/admin-escolar/asignaciones/<int:pk>/', views.admin_asignacion_detail, name='admin-asignacion-detail'),
    path('api/admin-escolar/asignaciones/materias-disponibles/', views.admin_materias_disponibles, name='admin-materias-disponibles'),
    path('api/admin-escolar/calificaciones/', views.admin_calificaciones_list, name='admin-calificaciones-list'),
    path('api/admin-escolar/calificaciones/<int:pk>/autorizar-cambio/', views.admin_calificacion_autorizar, name='admin-calificacion-autorizar'),
    path('api/admin-escolar/calificaciones/solicitudes/', views.admin_solicitudes_list, name='admin-solicitudes-list'),
    path('api/admin-escolar/calificaciones/solicitudes/<int:pk>/resolver/', views.admin_solicitud_resolver, name='admin-solicitud-resolver'),
    path('api/admin-escolar/periodos/', views.admin_periodos_list_create, name='admin-periodos-list'),
    path('api/admin-escolar/periodos/<int:pk>/', views.admin_periodo_detail, name='admin-periodo-detail'),
    path('api/admin-escolar/reporte-grupo/', views.admin_reporte_grupo_data, name='admin-reporte-grupo'),

    # Maestro
    path('api/maestro/asignaciones/', views.maestro_asignaciones_list, name='maestro-asignaciones-list'),
    path('api/maestro/estudiantes/', views.maestro_estudiantes_list, name='maestro-estudiantes-list'),
    path('api/maestro/estudiantes/grupos/', views.maestro_estudiantes_grupos, name='maestro-estudiantes-grupos'),
    path('api/maestro/calificaciones/', views.maestro_calificaciones_list_create, name='maestro-calificaciones-list'),
    path('api/maestro/calificaciones/<int:pk>/solicitar-cambio/', views.maestro_solicitar_cambio, name='maestro-solicitar-cambio'),
    path('api/maestro/calificaciones/grupo/<int:asignacion_id>/', views.maestro_calificaciones_grupo, name='maestro-calificaciones-grupo'),
    path('api/maestro/calificaciones/bulk/', views.maestro_calificaciones_bulk, name='maestro-calificaciones-bulk'),

    # Estudiante
    path('api/estudiante/historial/', views.estudiante_historial_view, name='estudiante-historial'),
    path('api/estudiante/historial/completo/', views.estudiante_historial_completo, name='estudiante-historial-completo'),
    path('api/estudiante/historial/pdf/', views.estudiante_calificaciones_pdf, name='estudiante-calificaciones-pdf'),
    path('api/academico/calendario/', views.calendario_eventos, name='calendario-eventos'),
]
