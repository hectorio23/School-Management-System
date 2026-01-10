from django.contrib import admin
from django.db.models import Q, Sum, F
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe
from decimal import Decimal
from comedor.models import AsistenciaCafeteria
from pagos.models import ConceptoPago, Adeudo, Pago

from .models import (
    Grado, Grupo, Estudiante, Tutor, EstudianteTutor,
    EstadoEstudiante, HistorialEstadosEstudiante,
    Estrato, HistorialEstratoEstudiante, EvaluacionSocioeconomica,
)



#########################################################
# FUNCIONES AUXILIARES
#########################################################

def generar_username_unico(nombre, apellido_paterno):
    """Genera un username único basado en nombre y apellido"""
    import random
    base = f"{nombre[:3]}{apellido_paterno[:3]}".lower()
    numero = random.randint(1000, 9999)
    username = f"{base}{numero}"
    
    # Verificar que sea único
    while Estudiante.objects.filter(nombre_usuario=username).exists():
        numero = random.randint(1000, 9999)
        username = f"{base}{numero}"
    
    return username


def calcular_estrato_sugerido(ingreso_mensual, miembros_hogar):
    """
    Calcula el estrato sugerido basado en ingreso per cápita
    
    Reglas (basadas en salario mínimo mexicano 2025: ~$250/día = ~$7,500/mes):
    - Ingreso per cápita < $2,000: Estrato A (50% descuento)
    - Ingreso per cápita $2,000-$4,000: Estrato B (30% descuento)
    - Ingreso per cápita $4,000-$6,000: Estrato C (15% descuento)
    - Ingreso per cápita > $6,000: Estrato D (0% descuento)
    """
    if miembros_hogar <= 0:
        miembros_hogar = 1
    
    ingreso_per_capita = ingreso_mensual / miembros_hogar
    
    try:
        if ingreso_per_capita < 2000:
            return Estrato.objects.filter(nombre='A').first()
        elif ingreso_per_capita < 4000:
            return Estrato.objects.filter(nombre='B').first()
        elif ingreso_per_capita < 6000:
            return Estrato.objects.filter(nombre='C').first()
        else:
            return Estrato.objects.filter(nombre='D').first()
    except:
        return None


#########################################################
# INLINES
#########################################################

class EstudianteTutorInline(admin.TabularInline):
    """Permite agregar/editar tutores directamente desde el estudiante"""
    model = EstudianteTutor
    extra = 1
    fields = ('tutor', 'parentesco', 'activo')
    autocomplete_fields = ['tutor']
    verbose_name = "Tutor"
    verbose_name_plural = "Tutores del estudiante"


class HistorialEstadosInline(admin.TabularInline):
    """Muestra el historial de estados (solo lectura, excepto el más reciente)"""
    model = HistorialEstadosEstudiante
    extra = 1
    fields = ('estado', 'justificacion')
    verbose_name = "Cambio de estado"
    verbose_name_plural = "Historial de estados"
    
    def get_readonly_fields(self, request, obj=None):
        # Solo el primero (más reciente) es editable
        if obj:
            return []
        return ['estado', 'justificacion']


class HistorialEstratoInline(admin.TabularInline):
    """Muestra el historial de estratos"""
    model = HistorialEstratoEstudiante
    extra = 1
    fields = ('estrato', )
    verbose_name = "Cambio de estrato"
    verbose_name_plural = "Historial de estratos"


class EvaluacionSocioeconomicaInline(admin.StackedInline):
    """Permite hacer evaluación socioeconómica directamente"""
    model = EvaluacionSocioeconomica
    extra = 0
    max_num = 1  # Solo una evaluación activa a la vez
    fields = (
        ('ingreso_mensual', 'miembros_hogar'),
        'tipo_vivienda',
        'documentos_json',
        ('aprobado'),
    )
    verbose_name = "Evaluación socioeconómica"
    verbose_name_plural = "Evaluación socioeconómica"



class AdeudoInline(admin.TabularInline):
    """Muestra los adeudos del estudiante"""
    model = Adeudo
    extra = 0
    fields = ('concepto', 'monto_base', 'descuento_aplicado', 'monto_final', 
              'fecha_vencimiento', 'estatus', 'saldo_display')
    readonly_fields = ['saldo_display', 'descuento_aplicado', 'monto_final']
    autocomplete_fields = ['concepto']
    verbose_name = "Adeudo"
    verbose_name_plural = "Adeudos del estudiante"
    
    def saldo_display(self, obj):
        if obj.id:
            saldo = obj.saldo_pendiente()
            color = 'red' if saldo > 0 else 'green'
            return format_html(
                '<span style="color: {}; font-weight: bold;">${:,.2f}</span>',
                color, saldo
            )
        return '-'
    saldo_display.short_description = 'Saldo pendiente'


class PagoInline(admin.TabularInline):
    """Muestra los pagos realizados"""
    model = Pago
    extra = 0
    fields = ('adeudo', 'monto', 'fecha_pago', 'metodo_pago', 'numero_referencia')
    readonly_fields = ['fecha_pago']
    autocomplete_fields = ['adeudo']
    verbose_name = "Pago realizado"
    verbose_name_plural = "Historial de pagos"


#########################################################
# ADMIN: GRADO
#########################################################

@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel', 'count_grupos')
    list_filter = ('nivel',)
    search_fields = ('nombre', 'nivel')
    ordering = ['nivel', 'nombre']
    
    fieldsets = (
        (None, {
            'fields': ('nombre', 'nivel')
        }),
    )
    
    def count_grupos(self, obj):
        count = obj.grupo_set.count()
        return f"{count} grupos"
    count_grupos.short_description = 'Grupos asociados'


#########################################################
# ADMIN: GRUPO
#########################################################

class EstudiantesEnGrupoInline(admin.TabularInline):
    """Permite asignar estudiantes al grupo directamente"""
    model = Estudiante
    extra = 0
    fields = ( 'nombre', 'apellido_paterno', 'apellido_materno', 'link_to_student')
    readonly_fields = ['link_to_student']
    verbose_name = "Estudiante en este grupo"
    verbose_name_plural = "Estudiantes en este grupo"
    fk_name = 'grupo'
    
    def link_to_student(self, obj):
        if obj.id:
            url = reverse('admin:estudiantes_estudiante_change', args=[obj.id])
            return format_html('<a href="{}" target="_blank">Ver detalles →</a>', url)
        return '-'
    link_to_student.short_description = 'Acciones'


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grado', 'generacion', 'count_estudiantes', 'fecha_creacion')
    list_filter = ('grado__nivel', 'grado', 'generacion')
    search_fields = ('nombre', 'generacion', 'descripcion')
    ordering = ['-generacion', 'grado__nivel', 'nombre']
    
    # Permite crear grado directamente desde aquí
    autocomplete_fields = ['grado']
    
    inlines = [EstudiantesEnGrupoInline]
    
    fieldsets = (
        ('Información del grupo', {
            'fields': ('nombre', 'grado', 'generacion', 'descripcion')
        }),
    )
    
    def count_estudiantes(self, obj):
        count = obj.estudiante_set.count()
        return f"{count} estudiantes"
    count_estudiantes.short_description = 'Total estudiantes'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Permite crear nuevo grado sin salir
        form.base_fields['grado'].widget.can_add_related = True
        form.base_fields['grado'].widget.can_change_related = True
        return form


#########################################################
# ADMIN: TUTOR
#########################################################

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'telefono', 'correo', 'count_estudiantes', 
                    'ultima_actualizacion_display')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'telefono')
    ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
    
    fieldsets = (
        ('Información personal', {
            'fields': (('nombre', 'apellido_paterno', 'apellido_materno'),
                      ('telefono', 'correo'))
        }),
        ('Control de actualización', {
            'fields': ('ultima_actualizacion', ),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ['ultima_actualizacion', 'fecha_creacion']
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    nombre_completo.short_description = 'Nombre completo'
    
    def count_estudiantes(self, obj):
        return obj.count_estudiantes()
    count_estudiantes.short_description = 'Estudiantes a cargo'
    
    def ultima_actualizacion_display(self, obj):
        if obj.ultima_actualizacion:
            return f"{obj.ultima_actualizacion.strftime('%d/%m/%Y %H:%M')}"
        return 'Nunca'
    ultima_actualizacion_display.short_description = 'Última actualización'


#########################################################
# ADMIN: ESTADO ESTUDIANTE
#########################################################

@admin.register(EstadoEstudiante)
class EstadoEstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_estado_activo', 'count_estudiantes')
    list_filter = ('es_estado_activo',)
    search_fields = ('nombre', 'descripcion')
    
    def count_estudiantes(self, obj):
        # Contar estudiantes con este estado actualmente
        count = HistorialEstadosEstudiante.objects.filter(
            estado=obj
        ).values('estudiante').distinct().count()
        return f"{count} estudiantes (histórico)"
    count_estudiantes.short_description = 'Uso'


#########################################################
# ADMIN: ESTRATO
#########################################################

@admin.register(Estrato)
class EstratoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje_descuento', 'activo', 'count_estudiantes')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    ordering = ['nombre']
    
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'porcentaje_descuento', 'activo')
        }),
    )
    
    def count_estudiantes(self, obj):
        count = HistorialEstratoEstudiante.objects.filter(
            estrato=obj
        ).values('estudiante').distinct().count()
        return f"{count} estudiantes (histórico)"
    count_estudiantes.short_description = 'Uso'


#########################################################
# ADMIN: CONCEPTO DE PAGO
#########################################################

@admin.register(ConceptoPago)
class ConceptoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monto_base', 'nivel_educativo', 'activo', 'count_adeudos')
    list_filter = ('nivel_educativo', 'activo')
    search_fields = ('nombre', 'descripcion')
    ordering = ['nivel_educativo', 'nombre']
    
    fieldsets = (
        ('Información del concepto', {
            'fields': ('nombre', 'descripcion', 'nivel_educativo')
        }),
        ('Configuración financiera', {
            'fields': ('monto_base', 'activo')
        }),
    )
    
    def count_adeudos(self, obj):
        count = obj.adeudo_set.count()
        return f"{count} adeudos generados"
    count_adeudos.short_description = 'Uso'


#########################################################
# ADMIN: ADEUDO
#########################################################

@admin.register(Adeudo)
class AdeudoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estudiante', 'concepto', 'monto_total', 'monto_pagado', 
                    'saldo_display', 'estatus', 'fecha_vencimiento', 'vencido_display')
    list_filter = ('estatus', 'fecha_vencimiento', 'concepto__nivel_educativo')
    search_fields = ('estudiante__matricula', 'estudiante__nombre', 
                    'estudiante__apellido_paterno', 'concepto__nombre')
    date_hierarchy = 'fecha_vencimiento'
    ordering = ['-fecha_generacion']
    
    autocomplete_fields = ['estudiante', 'concepto']
    
    readonly_fields = ['monto_final', 'monto_total', 'saldo_display', 'fecha_creacion', ]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('estudiante', 'concepto', 'estatus')
        }),
        ('Montos', {
            'fields': (
                'monto_base',
                'descuento_aplicado',
                'monto_final',
                'recargo_aplicado',
                'monto_total',
                'monto_pagado',
                'saldo_display',
            )
        }),
        ('Fechas', {
            'fields': ('fecha_generacion', 'fecha_vencimiento', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )
    
    inlines = [PagoInline]
    
    def saldo_display(self, obj):
        saldo = obj.saldo_pendiente()
        if saldo > 0:
            return mark_safe(
                '<span style="color: red; font-weight: bold;">${:,.2f}</span>',
                saldo
            )
        return mark_safe(
            '<span style="color: green; font-weight: bold;">$0.00 (PAGADO)</span>'
        )
    saldo_display.short_description = 'Saldo pendiente'
    
    def vencido_display(self, obj):
        if obj.esta_vencido():
            dias = (timezone.now().date() - obj.fecha_vencimiento).days
            return mark_safe(
                '<span style="color: red; font-weight: bold;">VENCIDO ({} días)</span>',
                dias
            )
        return mark_safe('<span style="color: green;">✓ Vigente</span>')
    vencido_display.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        # Calcular montos automáticamente si es nuevo
        if not change:
            # Obtener estrato actual del estudiante
            estrato = obj.estudiante.get_estrato_actual()
            
            if estrato:
                descuento = obj.monto_base * (estrato.porcentaje_descuento / 100)
                obj.descuento_aplicado = descuento
            else:
                obj.descuento_aplicado = 0
            
            obj.monto_final = obj.monto_base - obj.descuento_aplicado
            obj.monto_total = obj.monto_final + obj.recargo_aplicado
        
        super().save_model(request, obj, form, change)


#########################################################
# ADMIN: PAGO
#########################################################

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'adeudo', 'monto', 'fecha_pago', 'metodo_pago', 'recibido_por')
    list_filter = ('metodo_pago', 'fecha_pago')
    search_fields = ('adeudo__estudiante__matricula', 'adeudo__estudiante__nombre',
                    'numero_referencia', 'recibido_por')
    date_hierarchy = 'fecha_pago'
    ordering = ['-fecha_pago']
    
    autocomplete_fields = ['adeudo']
    
    readonly_fields = ['fecha_pago']
    
    fieldsets = (
        ('Información del pago', {
            'fields': ('adeudo', 'monto', 'metodo_pago', 'numero_referencia')
        }),
        ('Comprobante', {
            'fields': ('ruta_recibo', 'notas')
        }),
        ('Metadata', {
            'fields': ('recibido_por', 'fecha_pago'),
            'classes': ['collapse']
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Asignar quién recibió el pago
        if not obj.recibido_por:
            obj.recibido_por = request.user.username
        super().save_model(request, obj, form, change)


#########################################################
# ADMIN: ESTUDIANTE (EL MÁS IMPORTANTE)
#########################################################

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = (
        # 'matricula',
        'nombre_completo',
        'grupo',
        'estado_actual_display',
        'estrato_actual_display',
        'balance_display',
        'adeudos_vencidos_display',
    )
    
    list_filter = (
        'grupo__grado__nivel',
        'grupo__grado',
        'grupo',
    )
    
    search_fields = (
        'matricula',
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'nombre_usuario',
    )
    
    ordering = ['-fecha_creacion']
    
    # Permite crear grupo directamente desde aquí
    autocomplete_fields = ['grupo']
    
    readonly_fields = [
        'matricula',
        'fecha_creacion',
        'fecha_actualizacion',
        'estado_actual_display',
        'estrato_actual_display',
        'balance_display',
    ]
    
    inlines = [
        EstudianteTutorInline,
        EvaluacionSocioeconomicaInline,
        HistorialEstadosInline,
        HistorialEstratoInline,
        AdeudoInline,
    ]
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                # 'matricula',
                ('nombre', 'apellido_paterno', 'apellido_materno'),
                'direccion',
            )
        }),
        ('Información Académica', {
            'fields': ('grupo',)
        }),
        ('Acceso al Sistema', {
            'fields': (
                'nombre_usuario',
                'hash_contrasena',
                'digest_llave',
            ),
            'classes': ['collapse']
        }),
        ('Estado Actual', {
            'fields': (
                'estado_actual_display',
                'estrato_actual_display',
                'balance_display',
            ),
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ['collapse']
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Permitir crear grupo sin salir
        if 'grupo' in form.base_fields:
            form.base_fields['grupo'].widget.can_add_related = True
            form.base_fields['grupo'].widget.can_change_related = True
        
        return form
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    nombre_completo.short_description = 'Nombre completo'
    nombre_completo.admin_order_field = 'apellido_paterno'
    
    def estado_actual_display(self, obj):
        estado = obj.get_estado_actual()
        if estado:
            color = 'green' if estado.es_estado_activo else 'red'
            return mark_safe(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, estado.nombre
            )
        return mark_safe('<span style="color: gray;">Sin asignar</span>')
    estado_actual_display.short_description = 'Estado actual'
    
    def estrato_actual_display(self, obj):
        estrato = obj.get_estrato_actual()
        if estrato:
            return mark_safe(
                '<span style="font-weight: bold;">{} ({}% desc.)</span>',
                estrato.nombre, estrato.porcentaje_descuento
            )
        return mark_safe('<span style="color: gray;">Sin asignar</span>')
    estrato_actual_display.short_description = 'Estrato actual'
    
    def balance_display(self, obj):
        balance = obj.get_balance_total()
        if balance > 0:
            return mark_safe(
                '<span style="color: red; font-weight: bold;">${:,.2f}</span>',
                balance
            )
        return mark_safe('<span style="color: green;">$0.00</span>')
    balance_display.short_description = 'Balance total'
    
    def adeudos_vencidos_display(self, obj):
        vencidos = Adeudo.objects.filter(
            estudiante=obj,
            estatus__in=['pendiente', 'parcial'],
            fecha_vencimiento__lt=timezone.now().date()
        ).count()
        
        if vencidos > 0:
            return mark_safe(
                '<span style="color: red; font-weight: bold;">{} vencidos</span>',
                vencidos
            )
        return mark_safe('<span style="color: green;">✓ Al corriente</span>')
    adeudos_vencidos_display.short_description = 'Adeudos'
    
    def save_model(self, request, obj, form, change):
        # Si es nuevo estudiante
        if not change:
            # Generar username automáticamente si no existe
            if not obj.nombre_usuario:
                obj.nombre_usuario = generar_username_unico(obj.nombre, obj.apellido_paterno)
        
        super().save_model(request, obj, form, change)
        formset.save_m2m()


#########################################################
# CONFIGURACIÓN ADICIONAL
#########################################################

# Configurar búsqueda de autocomplete
@admin.register(EstudianteTutor)
class EstudianteTutorAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'tutor', 'parentesco', 'activo')
    list_filter = ('parentesco', 'activo')
    search_fields = ('estudiante__matricula', 'estudiante__nombre', 
                    'tutor__nombre', 'tutor__apellido_paterno')


# Personalizar el sitio de administración
admin.site.site_header = "Sistema de Gestión Escolar"
admin.site.site_title = "Admin Colegio"
admin.site.index_title = "Panel de Administración"