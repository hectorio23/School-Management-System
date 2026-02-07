from django.contrib import admin
from .models import (
    ProgramaEducativo, Materia, PeriodoEvaluacion, Maestro,
    AdministradorEscolar, AsignacionMaestro, Calificacion,
    CalificacionFinal, AutorizacionCambioCalificacion,
    ModificacionManualCalificacion
)

@admin.register(ProgramaEducativo)
class ProgramaEducativoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_educativo', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('nivel_educativo', 'activo')
    search_fields = ('nombre',)

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'clave', 'grado', 'programa_educativo', 'activa', 'orden')
    list_filter = ('grado', 'programa_educativo', 'activa')
    search_fields = ('nombre', 'clave')

@admin.register(PeriodoEvaluacion)
class PeriodoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_periodo', 'ciclo_escolar', 'programa_educativo', 'estatus', 'fecha_inicio_captura', 'fecha_fin_captura')
    list_filter = ('ciclo_escolar', 'estatus', 'programa_educativo')
    readonly_fields = ('fecha_inicio_captura', 'fecha_fin_captura')

@admin.register(Maestro)
class MaestroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'nivel_educativo', 'activo')
    list_filter = ('nivel_educativo', 'activo')
    search_fields = ('nombre', 'apellido_paterno', 'email')

@admin.register(AdministradorEscolar)
class AdministradorEscolarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'nivel_educativo', 'activo')
    list_filter = ('nivel_educativo', 'activo')
    search_fields = ('nombre', 'apellido_paterno', 'email')

@admin.register(AsignacionMaestro)
class AsignacionMaestroAdmin(admin.ModelAdmin):
    list_display = ('maestro', 'grupo', 'materia', 'ciclo_escolar', 'activa')
    list_filter = ('ciclo_escolar', 'activa')
    search_fields = ('maestro__nombre', 'grupo__nombre', 'materia__nombre')

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia_nombre', 'calificacion', 'periodo_evaluacion', 'puede_modificar')
    list_filter = ('periodo_evaluacion', 'puede_modificar')
    search_fields = ('estudiante__matricula', 'estudiante__nombre')

    def materia_nombre(self, obj):
        return obj.asignacion_maestro.materia.nombre

@admin.register(CalificacionFinal)
class CalificacionFinalAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia', 'ciclo_escolar', 'calificacion_final', 'estatus')
    list_filter = ('ciclo_escolar', 'estatus', 'materia')

@admin.register(AutorizacionCambioCalificacion)
class AutorizacionCambioCalificacionAdmin(admin.ModelAdmin):
    list_display = ('calificacion', 'autorizado_por', 'utilizada', 'fecha_autorizacion')
    list_filter = ('utilizada',)

@admin.register(ModificacionManualCalificacion)
class ModificacionManualCalificacionAdmin(admin.ModelAdmin):
    list_display = ('calificacion_final', 'modificado_por', 'valor_anterior', 'valor_nuevo', 'fecha_modificacion')
