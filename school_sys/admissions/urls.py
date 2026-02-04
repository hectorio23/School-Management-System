from django.urls import path
from . import views

urlpatterns = [
    # Auth / Registration
    path('register/initiate/', views.register_initiate, name='register_initiate'),
    path('register/confirm/', views.register_confirm, name='register_confirm'),
    path('login/', views.login_view, name='login_view'),
    # Phases
    path('aspirante/<int:folio>/phase1/', views.aspirante_phase1, name='aspirante_phase1'),
    path('aspirante/<int:folio>/phase2/', views.aspirante_phase2, name='aspirante_phase2'),
    path('aspirante/<int:folio>/phase3/', views.aspirante_phase3, name='aspirante_phase3'),
    path('dashboard/<int:folio>/', views.aspirante_dashboard, name='aspirante_dashboard'),
    path('aspirante/<int:folio>/contrato/', views.download_contrato, name='download_contrato'),
    # Admin
    path('admin/<int:folio>/mark-paid/', views.admin_mark_paid, name='admin_mark_paid'),
    path('admin/document/<int:folio>/<str:field_name>/', views.admin_view_document, name='admin_view_document'),
    path('admin/aspirante/<int:folio>/document/<str:field_name>/', views.admin_view_aspirante_document, name='admin_view_aspirante_document'),
    path('admin/tutor/<int:tutor_id>/document/<str:field_name>/', views.admin_view_tutor_document, name='admin_view_tutor_document'),
    # Migración de aspirantes a estudiantes
    path('admin/<int:folio>/migrate/', views.migrate_aspirante_to_student, name='migrate_aspirante'),
    path('admin/migrate-all/', views.migrate_all_accepted, name='migrate_all_accepted'),
    # Public Templates
    path('templates/<str:template_name>/', views.download_template, name='download_template'),
]
