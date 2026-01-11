from django.contrib import admin
from .models import AsistenciaCafeteria

@admin.register(AsistenciaCafeteria)
class AsistenciaCafeteriaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha_asistencia', 'tipo_comida', 'precio_aplicado')
    list_filter = ('fecha_asistencia', 'tipo_comida')
    # search_fields requiere que Estudiante tenga search_fields configurado (lo cual hicimos)
    search_fields = ('estudiante__nombre', 'estudiante__apellido_paterno', 'estudiante__matricula')
    date_hierarchy = 'fecha_asistencia'
    autocomplete_fields = ['estudiante']
    
    fieldsets = (
        ('Información de Asistencia', {
            'fields': ('estudiante', 'fecha_asistencia', 'tipo_comida')
        }),
        ('Detalles de Cobro', {
            'fields': ('precio_aplicado',)
        })
    )
