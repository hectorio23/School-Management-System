from django.contrib import admin
from .models import ConceptoPago, Adeudo, Pago
from .forms import ConceptoPagoForm

@admin.register(ConceptoPago)
class ConceptoPagoAdmin(admin.ModelAdmin):
    form = ConceptoPagoForm
    list_display = ('nombre', 'monto_base', 'activo', 'nivel_educativo')
    list_filter = ('activo', 'nivel_educativo')
    search_fields = ('nombre',)
    
    fieldsets = (
        ('Detalles del Concepto', {
            'fields': ('nombre', 'descripcion', 'monto_base', 'activo', 'nivel_educativo')
        }),
        ('Generación Automática de Adeudos', {
            'fields': ('aplicar_a_grado', 'aplicar_a_grupo', 'aplicar_a_estrato', 'aplicar_a_matricula'),
            'description': 'Use estos campos para generar automáticamente adeudos a los estudiantes seleccionados al guardar.',
            'classes': ('collapse',), # Opcional: colapsar si no se usa siempre
        }),
    )

@admin.register(Adeudo)
class AdeudoAdmin(admin.ModelAdmin):
    list_display = ('get_matricula', 'estudiante', 'concepto', 'get_monto_total', 'get_saldo_pendiente', 'estatus', 'fecha_vencimiento')
    list_filter = ('estatus', 'concepto', 'fecha_vencimiento')
    search_fields = ('estudiante__nombre', 'estudiante__apellido_paterno', 'estudiante__matricula', 'concepto__nombre')
    autocomplete_fields = ['estudiante', 'concepto']
    
    def get_matricula(self, obj):
        return obj.estudiante.matricula
    get_matricula.short_description = "Matrícula"
    
    def get_monto_total(self, obj):
        return f"${obj.monto_total}"
    get_monto_total.short_description = "Total"
    
    def get_saldo_pendiente(self, obj):
        return f"${obj.saldo_pendiente}"
    get_saldo_pendiente.short_description = "Pendiente"

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'adeudo', 'monto', 'fecha_pago', 'metodo_pago')
    list_filter = ('fecha_pago', 'metodo_pago')
    search_fields = ('adeudo__estudiante__nombre', 'referencia_bancaria')
    date_hierarchy = 'fecha_pago'
    autocomplete_fields = ['adeudo']
