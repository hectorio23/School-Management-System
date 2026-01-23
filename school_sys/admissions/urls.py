from django.urls import path
from . import views

urlpatterns = [
    # Auth / Registration
    path('register/initiate/', views.register_initiate, name='register_initiate'),
    path('register/confirm/', views.register_confirm, name='register_confirm'),
    # Phases
    path('me/<int:folio>/', views.aspirante_me, name='aspirante_me'),
    path('me/<int:folio>/phase1/', views.aspirante_phase1, name='aspirante_phase1'),
    path('me/<int:folio>/phase2/', views.aspirante_phase2, name='aspirante_phase2'),
    path('me/<int:folio>/phase3/', views.aspirante_phase3, name='aspirante_phase3'),
    # Admin
    path('admin/<int:folio>/mark-paid/', views.admin_mark_paid, name='admin_mark_paid'),
]
