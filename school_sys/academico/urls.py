from django.urls import path
from . import views

urlpatterns = [
    # Admin Escolar
    path('api/admin-escolar/maestros/', views.admin_maestros_list, name='admin-maestros-list'),
    path('api/admin-escolar/grupos/', views.admin_grupos_list, name='admin-grupos-list'),
    path('api/admin-escolar/materias/', views.admin_materias_list_create, name='admin-materias-list'),
    path('api/admin-escolar/materias/<int:pk>/desactivar/', views.admin_materia_desactivar, name='admin-materia-desactivar'),
    path('api/admin-escolar/asignaciones/', views.admin_asignaciones_list_create, name='admin-asignaciones-list'),
    path('api/admin-escolar/asignaciones/materias-disponibles/', views.admin_materias_disponibles, name='admin-materias-disponibles'),
    path('api/admin-escolar/calificaciones/', views.admin_calificaciones_list, name='admin-calificaciones-list'),
    path('api/admin-escolar/calificaciones/<int:pk>/autorizar-cambio/', views.admin_calificacion_autorizar, name='admin-calificacion-autorizar'),
    path('api/admin-escolar/periodos/', views.admin_periodos_list_create, name='admin-periodos-list'),

    # Maestro
    path('api/maestro/asignaciones/', views.maestro_asignaciones_list, name='maestro-asignaciones-list'),
    path('api/maestro/estudiantes/', views.maestro_estudiantes_list, name='maestro-estudiantes-list'),
    path('api/maestro/calificaciones/', views.maestro_calificaciones_list_create, name='maestro-calificaciones-list'),
    path('api/maestro/calificaciones/<int:pk>/solicitar-cambio/', views.maestro_solicitar_cambio, name='maestro-solicitar-cambio'),

    # Estudiante
    path('api/estudiante/historial/', views.estudiante_historial_view, name='estudiante-historial'),
]
