from django.urls import path
from . import views

urlpatterns = [
    # Libros
    path('libros/', views.libro_list_create_view, name='libro-list-create'),
    path('libros/<int:pk>/', views.libro_detail_view, name='libro-detail'),
    
    # Prestamos
    path('prestamos/realizar/', views.realizar_prestamo_view, name='realizar-prestamo'),
    path('prestamos/<int:pk>/devolver/', views.devolver_libro_view, name='devolver-libro'),
    
    # Multas
    path('multas/', views.multas_list_view, name='multas-list'),
    path('multas/<int:pk>/pagar/', views.pagar_multa_view, name='pagar-multa'),
    
    # Usuarios
    path('usuarios/', views.usuario_biblioteca_list_create_view, name='usuario-biblioteca-list'),
]
