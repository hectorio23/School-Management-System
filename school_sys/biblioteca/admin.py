from django.contrib import admin
from .models import Libro, UsuarioBiblioteca, Prestamo, Multa

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'numero_de_ejemplares', 'numero_de_ejemplares_prestados', 'ejemplares_disponibles')
    search_fields = ('titulo', 'autor', 'isbn')

@admin.register(UsuarioBiblioteca)
class UsuarioBibliotecaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'tipo_de_usuario')
    list_filter = ('tipo_de_usuario',)
    search_fields = ('nombre', 'apellido', 'email')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_de_prestamo', 'fecha_de_devolucion', 'estado')
    list_filter = ('estado', 'fecha_de_devolucion')
    date_hierarchy = 'fecha_de_prestamo'

@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'monto', 'estado', 'fecha_de_pago')
    list_filter = ('estado',)
