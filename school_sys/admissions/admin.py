from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import (
    AdmissionUser, AdmissionTutor, Aspirante, 
    AdmissionTutorAspirante, VerificationCode
)

# --- FORMS ---

class AdmissionUserForm(forms.ModelForm):
    class Meta:
        model = AdmissionUser
        fields = ('email', 'password')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Note: Primary key 'folio' is handled in model.save()
        if commit:
            instance.save()
        return instance

class AspiranteForm(forms.ModelForm):
    class Meta:
        model = Aspirante
        fields = '__all__'

# --- INLINES ---

class TutorAspiranteInline(admin.TabularInline):
    model = AdmissionTutorAspirante
    verbose_name = "Tutor"
    verbose_name_plural = "Vinculación de Tutores"
    fields = ('tutor', 'parentesco')
    extra = 1
    autocomplete_fields = ['tutor']

# --- ADMIN CLASSES ---

@admin.register(Aspirante)
class AdmisionAspiranteAdmin(admin.ModelAdmin):
    form = AspiranteForm
    list_display = ("get_folio", "nombre", "apellido_paterno", "curp", "status", "fase_actual", "pagado_status")
    list_filter = ("status", "fase_actual", "pagado_status", "sexo")
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'curp', 'user__folio', 'user__email')
    
    inlines = [TutorAspiranteInline]
    
    fieldsets = (
        ('Control de Admisión', {
            'fields': ('user', 'status', 'fase_actual', 'pagado_status')
        }),
        ('Fase 1: Información Personal', {
            'fields': (
                ('nombre', 'apellido_paterno', 'apellido_materno'),
                'curp', 'fecha_nacimiento', 'sexo',
                'direccion', 'telefono', 'escuela_procedencia', 'promedio_anterior'
            )
        }),
        ('Fase 2: Estudio Socioeconómico', {
            'fields': (
                'ingreso_mensual_familiar', ('ocupacion_padre', 'ocupacion_madre'),
                'tipo_vivienda', 'miembros_hogar', 'vehiculos', 'internet_encasa'
            )
        }),
        ('Fase 3: Documentación y Legal', {
            'fields': (
                'display_comprobante', 'comprobante_domicilio',
                'display_curp_pdf', 'curp_pdf',
                'display_acta_estudiante', 'acta_nacimiento_estudiante',
                'display_acta_tutor', 'acta_nacimiento_tutor',
                'display_curp_tutor', 'curp_tutor_pdf',
                ('acta_nacimiento_check', 'curp_check'),
                ('aceptacion_reglamento', 'autorizacion_imagen')
            )
        }),
        ('Fase 4: Información de Pago', {
            'fields': (
                'fecha_pago', 'monto', 'metodo_pago',
                'numero_referencia', 'ruta_recibo', 'recibido_por', 'notas'
            )
        }),
    )
    
    readonly_fields = (
        'display_comprobante', 'display_curp_pdf', 'display_acta_estudiante',
        'display_acta_tutor', 'display_curp_tutor'
    )

    def get_folio(self, obj):
        return obj.user.folio if obj.user else "-"
    get_folio.short_description = 'Folio'

    # --- FILE VIEW METHODS ---
    def _display_file(self, file_field):
        if file_field:
            return mark_safe(f'<a href="{file_field.url}" target="_blank">📄 Ver Documento</a>')
        return "No cargado"

    def display_comprobante(self, obj): return self._display_file(obj.comprobante_domicilio)
    display_comprobante.short_description = "Comprobante Domicilio Actual"
    
    def display_curp_pdf(self, obj): return self._display_file(obj.curp_pdf)
    display_curp_pdf.short_description = "CURP Aspirante (PDF)"
    
    def display_acta_estudiante(self, obj): return self._display_file(obj.acta_nacimiento_estudiante)
    display_acta_estudiante.short_description = "Acta Nacimiento Aspirante"
    
    def display_acta_tutor(self, obj): return self._display_file(obj.acta_nacimiento_tutor)
    display_acta_tutor.short_description = "Acta Nacimiento Tutor"
    
    def display_curp_tutor(self, obj): return self._display_file(obj.curp_tutor_pdf)
    display_curp_tutor.short_description = "CURP Tutor (PDF)"

@admin.register(AdmissionUser)
class AdmissionUserAdmin(admin.ModelAdmin):
    form = AdmissionUserForm
    list_display = ('folio', 'email', 'is_active', 'is_verified', 'date_joined')
    list_filter = ('is_active', 'is_verified')
    search_fields = ('folio', 'email')
    readonly_fields = ('folio', 'date_joined', 'password_mask')
    
    fieldsets = (
        ('Credenciales', {
            'fields': ('folio', 'email', 'password_mask')
        }),
        ('Estado de la Cuenta', {
            'fields': ('is_active', 'is_verified', 'date_joined')
        }),
    )

    def password_mask(self, obj):
        return "********"
    password_mask.short_description = "Contraseña (Segura)"

    def has_add_permission(self, request):
        return True # Permitir admin crear usuarios manualmente si lo desea

@admin.register(AdmissionTutor)
class AdmissionTutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'numero_telefono', 'curp')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'curp')

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at', 'expires_at', 'is_verified')
    readonly_fields = ('code', 'data_json', 'created_at', 'expires_at')

admin.site.register(AdmissionTutorAspirante)