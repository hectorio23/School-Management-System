from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import (
    AdmissionUser, AdmissionTutor, Aspirante, 
    AdmissionTutorAspirante, VerificationCode
)

from users.utils_export import generar_excel_aspirantes
from django.http import HttpResponse
# --- FORMULARIOS ---

class AdmissionUserForm(forms.ModelForm):
    """Formulario para la gestión de usuarios de admisión."""
    class Meta:
        model = AdmissionUser
        fields = ('email', 'password')

class AspiranteForm(forms.ModelForm):
    """Formulario integral del aspirante."""
    class Meta:
        model = Aspirante
        fields = '__all__'

# --- INLINES ---

class TutorAspiranteInline(admin.TabularInline):
    """Visualización de tutores vinculados en la ficha del aspirante."""
    model = AdmissionTutorAspirante
    verbose_name = "Tutor Vinculado"
    verbose_name_plural = "Tutores Vinculados"
    fields = ('tutor', 'parentesco', 'display_tutor_docs')
    readonly_fields = ('display_tutor_docs',)
    extra = 1
    autocomplete_fields = ['tutor']

    def display_tutor_docs(self, obj):
        """Muestra links rápidos a documentos del tutor desde la ficha del alumno."""
        if not obj.tutor: return "-"
        folio = obj.aspirante.user.folio
        links = []
        doc_map = {
            'acta_nacimiento_tutor': 'Acta',
            'ine_tutor': 'INE',
            'comprobante_domicilio_tutor': 'Domicilio'
        }
        for req_key, label in doc_map.items():
            url = reverse('admin_view_document', kwargs={'folio': folio, 'field_name': req_key})
            links.append(f'<a href="{url}" target="_blank" style="margin-right:10px;">📄 {label}</a>')
        return mark_safe(" ".join(links))
    display_tutor_docs.short_description = "Documentos Rápidos"

# --- CLASES ADMIN ---

@admin.register(Aspirante)
class AdmisionAspiranteAdmin(admin.ModelAdmin):
    """Panel de administración principal para el proceso de admisiones."""
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
        ('Fase 3: Documentación del Alumno (Encriptada)', {
            'fields': (
                ('display_foto', 'foto_credencial'),
                ('display_acta', 'acta_nacimiento'),
                ('display_curp', 'curp_pdf'),
                ('display_boleta_ant', 'boleta_ciclo_anterior'),
                ('display_boleta_act', 'boleta_ciclo_actual'),
                ('acta_nacimiento_check', 'curp_check'),
                ('aceptacion_reglamento', 'autorizacion_imagen')
            )
        }),
        ('Fase 4: Información de Pago (DESHABILITADA)', {
            'fields': (
                'fecha_pago', 'monto', 'metodo_pago',
                'numero_referencia', 'ruta_recibo', 'recibido_por', 'notas'
            ),
            'classes': ('collapse',),
        }),
        ('Evaluaciones Administrativas', {
            'fields': (
                'fecha_visita_domiciliaria',
                'fecha_entrevista_psicologia',
                'fecha_examen_pedagogico',
                'comentarios_analisis',
                'comentarios_comite'
            )
        }),
    )
    
    readonly_fields = (
        'display_foto', 'display_acta', 'display_curp', 
        'display_boleta_ant', 'display_boleta_act'
    )

    def get_folio(self, obj):
        return obj.user.folio if obj.user else "-"
    get_folio.short_description = 'Folio'

    # --- MÉTODOS DE VISUALIZACIÓN SEGURA ---
    
    def _get_secure_link(self, obj, field_name, label="Ver Archivo"):
        """Genera un link al visor seguro que desencripta en tiempo real."""
        if not obj or not obj.user: return "-"
        file_val = getattr(obj, field_name, None)
        if file_val:
            url = reverse('admin_view_document', kwargs={'folio': obj.user.folio, 'field_name': field_name})
            # Si es foto, podemos intentar un micro-preview directo al endpoint seguro
            if 'foto' in field_name:
                return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" style="height:50px; border-radius:5px; border:1px solid #ccc;"/><br/>🔍 Ampliar</a>')
            return mark_safe(f'<a href="{url}" target="_blank" class="button" style="background:#79aec8; color:white; padding:3px 10px; border-radius:3px;">📄 {label}</a>')
        return "Pendiente de subida"

    def display_foto(self, obj): return self._get_secure_link(obj, 'foto_credencial', "Fotografía")
    display_foto.short_description = "Vista Previa Foto"

    def display_acta(self, obj): return self._get_secure_link(obj, 'acta_nacimiento', "Acta Nacimiento")
    display_acta.short_description = "Documento Acta"

    def display_curp(self, obj): return self._get_secure_link(obj, 'curp_pdf', "CURP")
    display_curp.short_description = "Documento CURP"

    def display_boleta_ant(self, obj): return self._get_secure_link(obj, 'boleta_ciclo_anterior', "Boleta Anterior")
    display_boleta_ant.short_description = "Boleta Ciclo Anterior"

    def display_boleta_act(self, obj): return self._get_secure_link(obj, 'boleta_ciclo_actual', "Boleta Actual")
    display_boleta_act.short_description = "Boleta Ciclo Actual"

    actions = ["export_as_excel"]

    @admin.action(description="Exportar Lista de Aspirantes a Excel")
    def export_as_excel(self, request, queryset):
        buffer = generar_excel_aspirantes(queryset)
        if not buffer:
            self.message_user(request, "Error: Librería openpyxl no instalada.", level='ERROR')
            return
            
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="aspirantes.xlsx"'
        return response



@admin.register(AdmissionTutor)
class AdmissionTutorAdmin(admin.ModelAdmin):
    """Panel de administración para la gestión individual de tutores."""
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'curp')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'curp')
    
    fieldsets = (
        ('Datos de Identificación', {
            'fields': (('nombre', 'apellido_paterno', 'apellido_materno'), 'curp', 'email', 'numero_telefono')
        }),
        ('Documentación del Tutor (Encriptada)', {
            'fields': (
                ('display_ine', 'ine_tutor'),
                ('display_curp_pdf', 'curp_pdf'),
                ('display_domicilio', 'comprobante_domicilio'),
                ('display_fachada', 'foto_fachada_domicilio'),
                ('display_ingresos', 'comprobante_ingresos'),
                ('display_carta_ingresos', 'carta_ingresos'),
                ('display_contrato', 'contrato_arrendamiento_predial'),
                ('display_protesta', 'carta_bajo_protesta')
            )
        }),
    )
    
    readonly_fields = (
        'display_ine', 'display_curp_pdf', 'display_domicilio', 'display_fachada', 
        'display_ingresos', 'display_carta_ingresos', 'display_contrato', 'display_protesta'
    )

    def _get_tutor_secure_link(self, obj, field_name, label="Ver Documento"):
        """Genera link seguro buscando un folio asociado."""
        if not obj: return "-"
        # Buscamos al primer aspirante vinculado a este tutor para obtener un folio válido para el endpoint
        rel = AdmissionTutorAspirante.objects.filter(tutor=obj).first()
        if not rel: return "Tutor sin aspirante vinculado"
        
        # Mapeamos nombre del campo en el modelo al nombre que espera el endpoint (req_field)
        # El endpoint espera el nombre del campo del request (fase 3)
        mapping = {
            'acta_nacimiento': 'acta_nacimiento_tutor',
            'comprobante_domicilio': 'comprobante_domicilio_tutor',
            'foto_fachada_domicilio': 'foto_fachada_domicilio',
            'comprobante_ingresos': 'comprobante_ingresos',
            'carta_ingresos': 'carta_ingresos',
            'ine_tutor': 'ine_tutor',
            'contrato_arrendamiento_predial': 'contrato_arrendamiento_predial',
            'carta_bajo_protesta': 'carta_bajo_protesta'
        }
        req_field = mapping.get(field_name, field_name)
        
        url = reverse('admin_view_document', kwargs={'folio': rel.aspirante.user.folio, 'field_name': req_field})
        if 'foto' in field_name or 'fachada' in field_name:
             return mark_safe(f'<a href="{url}" target="_blank"><img src="{url}" style="height:50px; border-radius:5px; border:1px solid #ccc;"/><br/>🔍 Ver</a>')
        return mark_safe(f'<a href="{url}" target="_blank" class="button" style="background:#555; color:white; padding:2px 8px;">📄 {label}</a>')

    def display_ine(self, obj): return self._get_tutor_secure_link(obj, 'ine_tutor', "Identificación INE")
    def display_curp_pdf(self, obj): return self._get_tutor_secure_link(obj, 'curp_pdf', "Documento CURP")
    def display_domicilio(self, obj): return self._get_tutor_secure_link(obj, 'comprobante_domicilio', "Comprobante Domicilio")
    def display_fachada(self, obj): return self._get_tutor_secure_link(obj, 'foto_fachada_domicilio', "Foto Fachada")
    def display_ingresos(self, obj): return self._get_tutor_secure_link(obj, 'comprobante_ingresos', "Comprobante Ingresos")
    def display_carta_ingresos(self, obj): return self._get_tutor_secure_link(obj, 'carta_ingresos', "Carta Ingresos")
    def display_contrato(self, obj): return self._get_tutor_secure_link(obj, 'contrato_arrendamiento_predial', "Contrato / Predial")
    def display_protesta(self, obj): return self._get_tutor_secure_link(obj, 'carta_bajo_protesta', "Carta Protesta")


@admin.register(AdmissionUser)
class AdmissionUserAdmin(admin.ModelAdmin):
    """Panel de administración para cuentas de acceso de aspirantes."""
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

    def password_mask(self, obj): return "********"
    password_mask.short_description = "Contraseña (Segura)"

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    """Códigos MFA generados durante el registro."""
    list_display = ('email', 'code', 'created_at', 'expires_at', 'is_verified')
    readonly_fields = ('code', 'data_json', 'created_at', 'expires_at')

admin.site.register(AdmissionTutorAspirante)