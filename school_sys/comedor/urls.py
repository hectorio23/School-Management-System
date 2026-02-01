from django.urls import path
from . import views

urlpatterns = [
    path('admin/asistencias/', views.admin_asistencias_list, name='admin_asistencias_list'),
    path('admin/asistencias/registrar/', views.admin_registrar_asistencia, name='admin_registrar_asistencia'),
    path('admin/reportes/diario/', views.admin_reporte_diario, name='admin_reporte_diario'),
    path('admin/reportes/semanal/', views.admin_reporte_semanal, name='admin_reporte_semanal'),
    path('admin/reportes/mensual/', views.admin_reporte_mensual, name='admin_reporte_mensual'),
    path('admin/alergias/', views.admin_alertas_alergias, name='admin_alertas_alergias'),
    path('admin/estudiante/<str:matricula>/', views.admin_historial_asistencia_estudiante, name='admin_historial_asistencia'),
    
    # Menús
    path('admin/menus/', views.admin_menus_list, name='admin_menus_list'),
    path('admin/menu-semanal/', views.admin_menu_semanal, name='admin_menu_semanal'),
]
