from django.contrib import admin
from django.utils.html import format_html
from .models import ConceptoPago, Adeudo, Pago
from .forms import ConceptoPagoForm
from django.urls import reverse
from django.utils.html import format_html

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
            'fields': ('aplicar_a_nivel', 'aplicar_a_grado', 'aplicar_a_grupo', 'aplicar_a_estrato', 'aplicar_a_matricula'),
            'description': '''
                <strong>Use estos campos para generar automáticamente adeudos a los estudiantes seleccionados al guardar.</strong><br>
                El monto final se calcula como: <code>monto_base - (beca_% + estrato_%)</code><br>
                <ul>
                    <li><strong>Nivel Educativo:</strong> Primaria, Secundaria, Preparatoria</li>
                    <li><strong>Grado:</strong> Filtrar por grado específico</li>
                    <li><strong>Grupo:</strong> Filtrar por grupo específico</li>
                    <li><strong>Estrato:</strong> Filtrar adicionalmente por estrato socioeconómico</li>
                    <li><strong>Matrícula:</strong> Asignar a un solo estudiante (ignora los demás filtros)</li>
                </ul>
            ''',
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Sobrescribimos save_model para llamar explícitamente a la generación de adeudos
        después de que el concepto se haya guardado.
        """
        super().save_model(request, obj, form, change)
        form.generar_adeudos(obj)

@admin.register(Adeudo)
class AdeudoAdmin(admin.ModelAdmin):
    list_display = (
        'get_matricula', 'estudiante', 'concepto', 
        'get_monto_base', 'get_descuento', 'get_monto_total', 
        'get_saldo_pendiente', 'estatus', 'fecha_vencimiento', 'pagar_adeudo'
    )
    list_filter = ('estatus', 'concepto', 'fecha_vencimiento', 'estudiante__grupo__grado__nivel')
    search_fields = ('estudiante__nombre', 'estudiante__apellido_paterno', 'estudiante__matricula', 'concepto__nombre')
    autocomplete_fields = ['estudiante', 'concepto']
    ordering = ('-fecha_generacion',)
    
    readonly_fields = ('fecha_generacion', 'monto_pagado', 'monto_base', 'descuento_aplicado', 'recargo_aplicado', 'monto_total')
    
    fieldsets = (
        ('Estudiante y Concepto', {
            'fields': ('estudiante', 'concepto')
        }),
        ('Montos', {
            'fields': ('monto_base', 'descuento_aplicado', 'recargo_aplicado', 'monto_total', 'monto_pagado')
        }),
        ('Fechas y Estado', {
            'fields': ('fecha_generacion', 'fecha_vencimiento', 'estatus', 'mes_correspondiente')
        }),
        ('Configuración Avanzada', {
            'fields': ('recargo_exento', 'justificacion_exencion', 'generado_automaticamente', 'justificacion_manual'),
            'classes': ('collapse',)
        }),
    )
    
    def get_matricula(self, obj):
        return obj.estudiante.matricula
    get_matricula.short_description = "Matrícula"
    
    def get_monto_base(self, obj):
        return f"${float(obj.monto_base):,.2f}"
    get_monto_base.short_description = "Monto Base"
    
    def get_descuento(self, obj):
        descuento = float(obj.descuento_aplicado)
        if descuento > 0:
            return format_html('<span style="color: green;">-${}</span>', f"{descuento:,.2f}")
        return "-"
    get_descuento.short_description = "Descuento"
    
    def get_monto_total(self, obj):
        return f"${float(obj.monto_total):,.2f}"
    get_monto_total.short_description = "Total"
    
    def get_saldo_pendiente(self, obj):
        saldo = float(obj.monto_total) - float(obj.monto_pagado)
        if saldo > 0:
            return format_html('<span style="color: red;">${}</span>', f"{saldo:,.2f}")
        return format_html('<span style="color: green;">{}</span>', "$0.00")
    get_saldo_pendiente.short_description = "Pendiente"
    
    def pagar_adeudo(self, obj):
        saldo = float(obj.monto_total) - float(obj.monto_pagado)
        if saldo <= 0:
            return "-"
            
        url = reverse('admin:pagos_pago_add')
        return format_html(
            '<a class="button" href="{}?adeudo={}" style="background-color: #4ade80; color: white; padding: 3px 10px; border-radius: 4px; text-decoration: none;">Pagar</a>',
            url, obj.pk
        )
    pagar_adeudo.short_description = "Acciones"
    
    actions = ['recalcular_adeudos', 'registrar_pago_masivo']
    
    @admin.action(description="Recalcular montos y recargos de seleccionados")
    def recalcular_adeudos(self, request, queryset):
        for adeudo in queryset:
            adeudo.save()
        self.message_user(request, f"Se recalcularon {queryset.count()} adeudos.")

    @admin.action(description="Marcar como PAGADO (Dispara reinscripción)")
    def registrar_pago_masivo(self, request, queryset):
        with transaction.atomic():
            count = 0
            for adeudo in queryset:
                if adeudo.estatus != 'pagado':
                    adeudo.estatus = 'pagado'
                    adeudo.save() # Esto dispara el signal
                    count += 1
        self.message_user(request, f"Se marcaron {count} adeudos como pagados.")

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_estudiante', 'adeudo', 'monto', 'fecha_pago', 'metodo_pago')
    list_filter = ('fecha_pago', 'metodo_pago')
    search_fields = ('adeudo__estudiante__nombre', 'adeudo__estudiante__matricula', 'numero_referencia')
    # date_hierarchy = 'fecha_pago' # Comentado para evitar errores de zona horaria en DB sin soporte
    autocomplete_fields = ['adeudo']
    readonly_fields = ('recibido_por',) # Se llena automÃ¡ticamente
    change_list_template = 'admin/pagos/pago/change_list.html'
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # Edición
            return self.readonly_fields + ('adeudo',)
        return self.readonly_fields
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        adeudo_id = request.GET.get('adeudo')
        if adeudo_id:
            try:
                adeudo = Adeudo.objects.get(pk=adeudo_id)
                saldo = adeudo.monto_total - adeudo.monto_pagado
                initial['adeudo'] = adeudo_id
                initial['monto'] = saldo
            except (Adeudo.DoesNotExist, ValueError):
                pass
        return initial

    def get_estudiante(self, obj):
        return f"{obj.adeudo.estudiante.matricula} - {obj.adeudo.estudiante.nombre}"
    get_estudiante.short_description = "Estudiante"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "adeudo":
            # Filtrar solo adeudos que NO estÃ¡n pagados (pendiente, parcial, vencido)
            kwargs["queryset"] = Adeudo.objects.exclude(estatus='pagado')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # 1. Asignar usuario que recibe el pago
        if not obj.recibido_por:
            obj.recibido_por = request.user.email
            
        # 2. Si el monto es 0 o None, asignar el saldo pendiente del adeudo
        if not obj.monto or obj.monto == 0:
            if obj.adeudo: # Verificar que tenga adeudo asignado
                saldo_pendiente = obj.adeudo.monto_total - obj.adeudo.monto_pagado
                if saldo_pendiente > 0:
                    obj.monto = saldo_pendiente
                
        super().save_model(request, obj, form, change)
