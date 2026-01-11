from django.contrib import admin
from django.utils.timezone import now
from .models import (
    Estudiante, Tutor, EstudianteTutor, 
    Grado, Grupo, Estrato, EvaluacionSocioeconomica, 
    EstadoEstudiante, HistorialEstadosEstudiante
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


# --- Admins ---

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # Formulario personalizado para creación (User + Estudiante)
    add_form = EstudianteCreationForm
    
    list_display = ('matricula', 'get_nombre_completo', 'get_grado_grupo', 'get_estado_actual')
    # Removed 'estado_actual__nombre' because it's not a direct field
    list_filter = ('grupo__grado', 'grupo')
    search_fields = ('matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'usuario__email')
    ordering = ('apellido_paterno', 'apellido_materno')
    
    inlines = [EstudianteTutorInline, EvaluacionSocioeconomicaInline]
    
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


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'telefono', 'correo')
    search_fields = ('nombre', 'apellido_paterno', 'correo')


@admin.register(EvaluacionSocioeconomica)
class EvaluacionSocioeconomicaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'estrato', 'ingreso_mensual', 'fecha_evaluacion', 'aprobado')
    list_filter = ('estrato', 'aprobado', 'fecha_evaluacion')
    search_fields = ('estudiante__nombre', 'estudiante__matricula')
    ordering = ('-fecha_evaluacion',)
    autocomplete_fields = ['estudiante']
    
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
