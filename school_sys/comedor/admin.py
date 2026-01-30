from django.contrib import admin
from django.utils import timezone
from .models import AsistenciaCafeteria, Menu, MenuSemanal, AdeudoComedor
from pagos.models import Adeudo
from django.db import transaction
from django.db.models import F

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'precio', 'desactivar')
    list_filter = ('desactivar',) 
    search_fields = ('descripcion',)

@admin.register(MenuSemanal)
class MenuSemanalAdmin(admin.ModelAdmin):
    list_display = ('semana_inicio', 'semana_fin', 'descripcion', 'activo')
    search_fields = ('descripcion', 'semana_inicio')
    list_filter = ('activo',)

@admin.register(AsistenciaCafeteria)
class AsistenciaCafeteriaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha_asistencia', 'tipo_comida', 'precio_aplicado', 'fecha_registro')
    list_filter = ('fecha_asistencia', 'tipo_comida')
    search_fields = ('estudiante__nombre', 'estudiante__apellido_paterno', 'estudiante__matricula')
    date_hierarchy = 'fecha_asistencia'
    autocomplete_fields = ['estudiante', 'menu']
    
    fieldsets = (
        ('Información de Asistencia', {
            'fields': ('estudiante', 'fecha_asistencia', 'tipo_comida', 'menu')
        }),
        ('Detalles de Cobro', {
            'fields': ('precio_aplicado',)
        })
    )

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        
        if not obj.precio_aplicado:
            if obj.menu:
                obj.precio_aplicado = obj.menu.precio
            else:
                 obj.precio_aplicado = 10.00

        with transaction.atomic():
            super().save_model(request, obj, form, change)
            
            if is_new:
                if not hasattr(obj, 'adeudo_comedor'):
                    AdeudoComedor.objects.create(
                        estudiante=obj.estudiante,
                        asistencia=obj,
                        monto=obj.precio_aplicado
                    )
                    self.message_user(request, "Se generó automáticamente el adeudo de comedor.")


@admin.register(AdeudoComedor)
class AdeudoComedorAdmin(admin.ModelAdmin):
    list_display = (
        'estudiante', 'monto', 'fecha_generacion', 
        'fecha_vencimiento', 'get_pagado', 'get_recargo_display'
    )
    # cambiamos pagado por el campo del modelo relacionado
    list_filter = ('adeudo__estatus', 'fecha_generacion', 'fecha_vencimiento')
    search_fields = ('estudiante__nombre', 'estudiante__apellido_paterno', 'estudiante__matricula')
    autocomplete_fields = ['estudiante', 'asistencia']
    
    readonly_fields = ('fecha_generacion', 'recargo_aplicado', 'monto_total', 'adeudo')
    
    actions = ['marcar_como_pagado']
    
    def get_recargo_display(self, obj):
        return obj.recargo_aplicado
    get_recargo_display.short_description = "Recargo Aplicado"
    
    def get_pagado(self, obj):
        return obj.pagado
    get_pagado.boolean = True
    get_pagado.short_description = "Pagado"
    get_pagado.admin_order_field = 'adeudo__estatus'
    
    @admin.action(description="Marcar adeudos seleccionados como PAGADOS")
    def marcar_como_pagado(self, request, queryset):
        # Actualizamos la tabla relacionada Adeudo
        # Obtenemos los IDs de los adeudos principales
        adeudos_ids = queryset.values_list('adeudo', flat=True)
        
        updated = Adeudo.objects.filter(id__in=adeudos_ids).update(
            estatus='pagado', 
            monto_pagado=F('monto_total')
        )
        self.message_user(request, f"Se marcaron {updated} adeudos principales como pagados.")
