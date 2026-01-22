from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/send-code/', views.auth_send_code, name='auth_send_code'),
    path('auth/verify-code/', views.auth_verify_code, name='auth_verify_code'),
    path('register/', views.register_aspirante, name='register_aspirante'),
    # Phases
    path('me/<int:folio>/', views.aspirante_me, name='aspirante_me'),
    path('me/<int:folio>/phase1/', views.aspirante_phase1, name='aspirante_phase1'),
    path('me/<int:folio>/phase2/', views.aspirante_phase2, name='aspirante_phase2'),
    path('me/<int:folio>/phase3/', views.aspirante_phase3, name='aspirante_phase3'),
    # Admin
    path('admin/<int:folio>/mark-paid/', views.admin_mark_paid, name='admin_mark_paid'),
]
