from django.contrib import admin
from .models import AsistenciaCafeteria, Menu, MenuSemanal
from pagos.models import Adeudo

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'desactivar')
    list_filter = ('desactivar',) 
    search_fields = ('descripcion',)

@admin.register(MenuSemanal)
class MenuSemanalAdmin(admin.ModelAdmin):
    list_display = ('semana_inicio', 'semana_fin', 'descripcion', 'activo')
    search_fields = ('descripcion', 'semana_inicio')
    list_filter = ('activo',)

@admin.register(AsistenciaCafeteria)
class AsistenciaCafeteriaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha_asistencia', 'tipo_comida', 'precio_aplicado', 'get_adeudo_status', 'fecha_registro')
    list_filter = ('fecha_asistencia', 'tipo_comida', 'adeudo__estatus')
    search_fields = ('estudiante__nombre', 'estudiante__apellido_paterno', 'estudiante__matricula')
    date_hierarchy = 'fecha_asistencia'
    autocomplete_fields = ['estudiante', 'menu']
    readonly_fields = ('precio_aplicado', 'fecha_registro', 'adeudo')
    
    fieldsets = (
        ('Información de Asistencia', {
            'fields': ('estudiante', 'fecha_asistencia', 'tipo_comida', 'menu')
        }),
        ('Vinculación Contable', {
            'fields': ('adeudo',)
        })
    )

    def get_adeudo_status(self, obj):
        if obj.adeudo:
            return obj.adeudo.estatus.upper()
        return "SIN ADEUDO"
    get_adeudo_status.short_description = "Estado de Pago"
