from django.contrib import admin
from django.utils.timezone import now
from django.utils.html import format_html
from django.db import models
from .models import (
    Estudiante, Tutor, EstudianteTutor,
    NivelEducativo, Grado, Grupo, CicloEscolar,
    EstadoEstudiante, HistorialEstadosEstudiante,
    Estrato, EvaluacionSocioeconomica,
    Beca, BecaEstudiante, Inscripcion
)
from .forms import EstudianteCreationForm
from .services import generar_adeudos_reinscripcion, asegurar_grupos_ciclo
from django.utils import timezone

from users.utils_export import generar_excel_estudiantes
from django.http import HttpResponse
from users.utils_export import generar_pdf_estudiantes
        

# --- Inlines ---

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    autocomplete_fields = ['grupo']
    readonly_fields = ('fecha_inscripcion',)
    verbose_name = "Historial de Inscripción"
    verbose_name_plural = "Historial de Inscripciones"


class EstudianteTutorInline(admin.TabularInline):
    model = EstudianteTutor
    extra = 1
    autocomplete_fields = ['tutor']
    verbose_name = "Tutor Asignado"
    verbose_name_plural = "Tutores Asignados"


class EstudianteTutorInlineForTutor(admin.TabularInline):
    model = EstudianteTutor
    extra = 0
    autocomplete_fields = ['estudiante']
    verbose_name = "Estudiante Asignado"
    verbose_name_plural = "Estudiantes Asignados"
    readonly_fields = ('get_matricula', 'get_grado_grupo')
    fields = ('estudiante', 'get_matricula', 'get_grado_grupo', 'parentesco', 'activo')
    
    def get_matricula(self, obj):
        if obj.estudiante:
            return obj.estudiante.matricula
        return "-"
    get_matricula.short_description = "Matrícula"
    
    def get_grado_grupo(self, obj):
        if obj.estudiante:
            inscripcion = obj.estudiante.inscripciones.filter(ciclo_escolar__activo=True).first()
            if inscripcion and inscripcion.grupo:
                return f"{inscripcion.grupo.grado} - {inscripcion.grupo.nombre}"
        return "-"
    get_grado_grupo.short_description = "Grado y Grupo"


class EvaluacionSocioeconomicaInline(admin.TabularInline):
    model = EvaluacionSocioeconomica
    extra = 0
    ordering = ('-fecha_evaluacion',)
    readonly_fields = ('fecha_evaluacion',)
    can_delete = False
    
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_add_permission(self, request, obj=None):
        return True


class BecaEstudianteInline(admin.TabularInline):
    model = BecaEstudiante
    extra = 0
    autocomplete_fields = ['beca']
    readonly_fields = ('fecha_asignacion', 'fecha_retiro')
    verbose_name = "Beca Asignada"
    verbose_name_plural = "Becas Asignadas"


class BecaEstudianteInlineForBeca(admin.TabularInline):
    model = BecaEstudiante
    extra = 1
    autocomplete_fields = ['estudiante']
    readonly_fields = ('fecha_asignacion', 'get_matricula', 'get_grado_grupo')
    fields = ('estudiante', 'get_matricula', 'get_grado_grupo', 'activa', 'fecha_asignacion', 'fecha_retiro', 'motivo_retiro')
    verbose_name = "Estudiante con Beca"
    verbose_name_plural = "Estudiantes con Beca"
    
    def get_matricula(self, obj):
        if obj.estudiante:
            return obj.estudiante.matricula
        return "-"
    get_matricula.short_description = "Matrícula"
    
    def get_grado_grupo(self, obj):
        if obj.estudiante:
            inscripcion = obj.estudiante.inscripciones.filter(ciclo_escolar__activo=True).first()
            if inscripcion and inscripcion.grupo:
                return f"{inscripcion.grupo.grado} - {inscripcion.grupo.nombre}"
        return "-"
    get_grado_grupo.short_description = "Grado y Grupo"


# --- Admins ---

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    add_form = EstudianteCreationForm
    
    list_display = ('matricula', 'get_nombre_completo', 'get_grado_grupo', 'get_estado_actual', 'get_estrato_display', 'get_beca_display')
    list_filter = (
        'inscripciones__grupo__ciclo_escolar', 
        'inscripciones__grupo__grado',
        'inscripciones__estatus'
    )
    search_fields = ('matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'usuario__email')
    ordering = ('apellido_paterno', 'apellido_materno')
    
    inlines = [InscripcionInline, EstudianteTutorInline, EvaluacionSocioeconomicaInline, BecaEstudianteInline]

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno', 'direccion',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno', 'direccion'),
        }),
        ('Credenciales de Acceso', {
            'fields': ('email_usuario', 'username_usuario', 'password_usuario'),
        }),
        ('Inscripción Inicial', {
            'fields': ('ciclo_escolar', 'grupo'),
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    get_nombre_completo.short_description = "Nombre Completo"
    
    def get_grado_grupo(self, obj):
        inscripcion = obj.inscripciones.filter(ciclo_escolar__activo=True).first()
        if inscripcion and inscripcion.grupo:
            return str(inscripcion.grupo)
        return "-"
    get_grado_grupo.short_description = "Ciclo Activo"

    def get_estado_actual(self, obj):
        inscripcion = obj.inscripciones.filter(ciclo_escolar__activo=True).first()
        if inscripcion:
            return inscripcion.get_estatus_display()
        return "NO INSCRITO"
    get_estado_actual.short_description = "Estado"

    def get_estrato_display(self, obj):
        estrato = obj.get_estrato_actual()
        if estrato:
            return format_html(
                '<span style="padding: 2px 8px; border-radius: 12px; background-color: {color}; color: white; font-weight: bold;">{nombre} ({desc}%)</span>',
                color=estrato.color or "#6B7280",
                nombre=estrato.nombre,
                desc=estrato.porcentaje_descuento
            )
        return "-"
    get_estrato_display.short_description = "Estrato"

    def get_beca_display(self, obj):
        beca = obj.get_beca_activa()
        if beca:
            return format_html('<span style="color: green; font-weight: bold;">{} ({}%)</span>', beca.nombre, beca.porcentaje)
        return "-"
    get_beca_display.short_description = "Beca Activa"

    actions = ["export_as_excel", "export_as_pdf"]

    @admin.action(description="Exportar a Excel")
    def export_as_excel(self, request, queryset):
        buffer = generar_excel_estudiantes(queryset)
        if not buffer:
            self.message_user(request, "Error: Librería openpyxl no instalada.", level='ERROR')
            return
            
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.xlsx"'
        return response

    @admin.action(description="Exportar a PDF")
    def export_as_pdf(self, request, queryset):
        buffer = generar_pdf_estudiantes(queryset)
        if not buffer:
             self.message_user(request, "Error: Librería reportlab no instalada.", level='ERROR')
             return

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.pdf"'
        return response


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'telefono', 'correo', 'get_estudiantes_count')
    search_fields = ('nombre', 'apellido_paterno', 'correo')
    inlines = [EstudianteTutorInlineForTutor]
    
    def get_estudiantes_count(self, obj):
        return obj.count_estudiantes()
    get_estudiantes_count.short_description = "Estudiantes"


@admin.register(EvaluacionSocioeconomica)
class EvaluacionSocioeconomicaAdmin(admin.ModelAdmin):
    list_display = ('get_matricula', 'estudiante', 'estrato', 'ingreso_mensual', 'fecha_evaluacion', 'aprobado')
    list_filter = ('estrato', 'aprobado', 'fecha_evaluacion')
    search_fields = ('estudiante__nombre', 'estudiante__matricula')
    ordering = ('-fecha_evaluacion',)
    autocomplete_fields = ['estudiante']
    
    def get_matricula(self, obj):
        return obj.estudiante.matricula
    get_matricula.short_description = "Matrícula"
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.pk = None
            obj.fecha_evaluacion = now()
        super().save_model(request, obj, form, change)


@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_educativo', 'numero_grado', 'orden_global')
    list_filter = ('nivel_educativo',)
    ordering = ('orden_global',)
    exclude = ('nivel',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grado', 'ciclo_escolar', 'capacidad_maxima')
    list_filter = ('grado', 'ciclo_escolar')
    search_fields = ('nombre', 'grado__nombre')
    exclude = ('generacion',)


@admin.register(NivelEducativo)
class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'grados_totales')
    search_fields = ('nombre',)
    ordering = ('orden',)


@admin.register(CicloEscolar)
class CicloEscolarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'activo')
    list_editable = ('activo',)
    search_fields = ('nombre',)

    def save_model(self, request, obj, form, change):
        
        se_activo = obj.activo and (not change or not CicloEscolar.objects.get(pk=obj.pk).activo)
        super().save_model(request, obj, form, change)

        if se_activo:
            grupos_creados = asegurar_grupos_ciclo(obj)
            ciclo_anterior = CicloEscolar.objects.filter(activo=False).exclude(pk=obj.pk).order_by('-fecha_fin').first()
            
            adeudos_msg = ""
            if ciclo_anterior:
                resultados = generar_adeudos_reinscripcion(ciclo_anterior)
                adeudos_msg = f" y se generaron {resultados['adeudos_creados']} adeudos"

            self.message_user(request, f"Ciclo {obj.nombre} activado. Se crearon {grupos_creados} grupos{adeudos_msg}.")


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'grupo', 'ciclo_escolar', 'estatus', 'fecha_inscripcion')
    list_filter = ('grupo__ciclo_escolar', 'estatus', 'grupo__grado')
    search_fields = ('estudiante__nombre', 'estudiante__matricula')
    autocomplete_fields = ['estudiante', 'grupo']


@admin.register(Estrato)
class EstratoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje_descuento', 'descripcion')


@admin.register(EstadoEstudiante)
class EstadoEstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'es_estado_activo')


# --- Admin de Becas ---

@admin.register(Beca)
class BecaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje', 'fecha_inicio', 'fecha_vencimiento', 'valida', 'get_estudiantes_count')
    list_filter = ('valida', 'fecha_inicio', 'fecha_vencimiento')
    search_fields = ('nombre', 'descripcion')
    ordering = ('-valida', '-fecha_inicio')
    inlines = [BecaEstudianteInlineForBeca]
    
    fieldsets = (
        ('Información de la Beca', {
            'fields': ('nombre', 'descripcion', 'porcentaje')
        }),
        ('Vigencia', {
            'fields': ('fecha_inicio', 'fecha_vencimiento', 'valida')
        }),
    )
    
    def get_estudiantes_count(self, obj):
        return obj.becaestudiante_set.filter(activa=True).count()
    get_estudiantes_count.short_description = "Estudiantes con Beca"
    
    actions = ['verificar_vigencia', 'marcar_como_vencida']
    
    @admin.action(description="Verificar vigencia de becas seleccionadas")
    def verificar_vigencia(self, request, queryset):
        for beca in queryset:
            beca.verificar_vigencia()
        self.message_user(request, f"Se verificó la vigencia de {queryset.count()} becas.")
    
    @admin.action(description="Marcar becas como vencidas")
    def marcar_como_vencida(self, request, queryset):
        queryset.update(valida=False)
        self.message_user(request, f"Se marcaron {queryset.count()} becas como vencidas.")


@admin.register(BecaEstudiante)
class BecaEstudianteAdmin(admin.ModelAdmin):
    list_display = ('get_matricula', 'estudiante', 'beca', 'get_porcentaje', 'activa', 'fecha_asignacion', 'fecha_retiro')
    list_filter = ('activa', 'beca', 'fecha_asignacion')
    search_fields = ('estudiante__nombre', 'estudiante__matricula', 'beca__nombre')
    autocomplete_fields = ['estudiante', 'beca']
    ordering = ('-fecha_asignacion',)
    
    readonly_fields = ('fecha_asignacion',)
    
    fieldsets = (
        ('Asignación', {
            'fields': ('beca', 'estudiante', 'activa')
        }),
        ('Fechas', {
            'fields': ('fecha_asignacion', 'fecha_retiro')
        }),
        ('Retiro', {
            'fields': ('motivo_retiro', 'asignado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def get_matricula(self, obj):
        return obj.estudiante.matricula
    get_matricula.short_description = "Matrícula"
    
    def get_porcentaje(self, obj):
        return f"{obj.beca.porcentaje}%"
    get_porcentaje.short_description = "% Descuento"
    
    actions = ['retirar_becas', 'activar_becas']
    
    @admin.action(description="Retirar becas seleccionadas")
    def retirar_becas(self, request, queryset):
        queryset.update(activa=False, fecha_retiro=timezone.now(), motivo_retiro="Retiro masivo desde admin")
        self.message_user(request, f"Se retiraron {queryset.count()} asignaciones de beca.")
    
    @admin.action(description="Activar becas seleccionadas")
    def activar_becas(self, request, queryset):
        queryset.update(activa=True, fecha_retiro=None, motivo_retiro=None)
        self.message_user(request, f"Se activaron {queryset.count()} asignaciones de beca.")
