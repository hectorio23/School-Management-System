from django.contrib import admin
from django.utils.timezone import now
from django.utils.html import format_html
from django import forms
from .models import (
    Estudiante, Tutor, EstudianteTutor, 
    Grado, Grupo, Estrato, EvaluacionSocioeconomica, 
    EstadoEstudiante, HistorialEstadosEstudiante,
    Beca, BecaEstudiante
)
from .forms import EstudianteCreationForm

# --- Inlines ---

class EstudianteTutorInline(admin.TabularInline):
    """
    Permite gestionar la relación M2M entre Estudiante y Tutor
    directamente desde la vista del estudiante.
    Incluye los campos extra de la tabla intermedia (parentesco, activo).
    """
    model = EstudianteTutor
    extra = 1
    autocomplete_fields = ['tutor'] # Requiere search_fields en TutorAdmin
    verbose_name = "Tutor Asignado"
    verbose_name_plural = "Tutores Asignados"


class EstudianteTutorInlineForTutor(admin.TabularInline):
    """
    Muestra los estudiantes asociados a un tutor desde la vista del tutor.
    """
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
        if obj.estudiante and obj.estudiante.grupo:
            return f"{obj.estudiante.grupo.grado} - {obj.estudiante.grupo.nombre}"
        return "-"
    get_grado_grupo.short_description = "Grado y Grupo"


class EvaluacionSocioeconomicaInline(admin.TabularInline):
    """
    Muestra el historial de evaluaciones socioeconómicas.
    Se recomienda usar 'can_delete = False' para preservar historial,
    o manejarlo con cuidado.
    """
    model = EvaluacionSocioeconomica
    extra = 0
    ordering = ('-fecha_evaluacion',)
    readonly_fields = ('fecha_evaluacion',) # Fecha inmutable una vez creada
    can_delete = False
    
    def has_change_permission(self, request, obj=None):
        # Evitar edición directa en inline para forzar creación de nuevo registro
        # o permitirlo si se desea corregir errores menores.
        return False
        
    def has_add_permission(self, request, obj=None):
        return True


class BecaEstudianteInline(admin.TabularInline):
    """
    Muestra las becas asignadas a un estudiante.
    """
    model = BecaEstudiante
    extra = 0
    autocomplete_fields = ['beca']
    readonly_fields = ('fecha_asignacion', 'fecha_retiro')
    verbose_name = "Beca Asignada"
    verbose_name_plural = "Becas Asignadas"


class BecaEstudianteInlineForBeca(admin.TabularInline):
    """
    Muestra los estudiantes asignados a una beca desde la vista de la beca.
    """
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
        if obj.estudiante and obj.estudiante.grupo:
            return f"{obj.estudiante.grupo.grado} - {obj.estudiante.grupo.nombre}"
        return "-"
    get_grado_grupo.short_description = "Grado y Grupo"


# --- Admins ---

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # Formulario personalizado para creación (User + Estudiante)
    add_form = EstudianteCreationForm
    
    list_display = ('matricula', 'get_nombre_completo', 'get_grado_grupo', 'get_estado_actual', 'get_beca_display')
    # Removed 'estado_actual__nombre' because it's not a direct field
    list_filter = ('grupo__grado', 'grupo')
    search_fields = ('matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'usuario__email')
    ordering = ('apellido_paterno', 'apellido_materno')
    
    inlines = [EstudianteTutorInline, EvaluacionSocioeconomicaInline, BecaEstudianteInline]
    
    # Campos a mostrar en detalle
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno', 'direccion',) # Check models for 'fecha_nacimiento' availability, assuming removed if error
        }),
        ('Información Académica', {
            'fields': ('grupo',) 
        }),
        # Matricula y Usuario se excluyen o son readonly
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Usa el formulario personalizado solo al crear (add_view).
        Al editar, usa el formulario por defecto del ModelAdmin.
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    # Helpers para list_display
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    get_nombre_completo.short_description = "Nombre Completo"
    
    def get_grado_grupo(self, obj):
        if obj.grupo:
            return f"{obj.grupo.grado} - {obj.grupo.nombre}"
        return "-"
    get_grado_grupo.short_description = "Grado y Grupo"

    def get_estado_actual(self, obj):
        return obj.get_estado_actual()
    get_estado_actual.short_description = "Estado"

    def get_beca_display(self, obj):
        beca = obj.get_beca_activa()
        if beca:
            return format_html('<span style="color: green;">{} ({}%)</span>', beca.nombre, beca.porcentaje)
        return "-"
    get_beca_display.short_description = "Beca Activa"


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
        """
        Lógica para Historial:
        Si se actualiza un registro existente (change=True),
        creamos uno NUEVO en lugar de sobrescribir el anterior.
        """
        if change:
            # Forzamos creación de nuevo registro
            obj.pk = None
            obj.fecha_evaluacion = now() # Actualizamos fecha al momento actual
        
        super().save_model(request, obj, form, change)


@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel')
    list_filter = ('nivel',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grado', 'generacion')
    list_filter = ('grado', 'generacion')


@admin.register(Estrato)
class EstratoAdmin(admin.ModelAdmin):
    # Removed 'nivel' from list_display as per error fix
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
    # date_hierarchy = 'fecha_inicio' # Comentado por error de zona horaria
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
    # date_hierarchy = 'fecha_asignacion' # Comentado por error de zona horaria
    
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
        from django.utils import timezone
        queryset.update(activa=False, fecha_retiro=timezone.now(), motivo_retiro="Retiro masivo desde admin")
        self.message_user(request, f"Se retiraron {queryset.count()} asignaciones de beca.")
    
    @admin.action(description="Activar becas seleccionadas")
    def activar_becas(self, request, queryset):
        queryset.update(activa=True, fecha_retiro=None, motivo_retiro=None)
        self.message_user(request, f"Se activaron {queryset.count()} asignaciones de beca.")
