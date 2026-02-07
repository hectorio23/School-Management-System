from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from users.models import User
from estudiantes.models import NivelEducativo, Grado, CicloEscolar, Grupo, Estudiante

class ProgramaEducativo(models.Model):
    """
    Representa los programas académicos (PREESCOLAR, PRIMARIA, SECUNDARIA).
    """
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.PROTECT, related_name='programas_educativos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    numero_periodos_evaluacion = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(4)],
        help_text="3 o 4 períodos por ciclo"
    )
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programas_educativos'
        indexes = [
            models.Index(fields=['nivel_educativo'], name='idx_programa_nivel'),
            models.Index(fields=['activo'], name='idx_programa_activo'),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Un nivel educativo solo puede tener UN programa activo a la vez
        if self.activo:
            ProgramaEducativo.objects.filter(
                nivel_educativo=self.nivel_educativo, activo=True
            ).exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)


class Materia(models.Model):
    """
    Define las materias que se cursan en cada grado.
    """
    grado = models.ForeignKey(Grado, on_delete=models.PROTECT, related_name='materias')
    programa_educativo = models.ForeignKey(ProgramaEducativo, on_delete=models.PROTECT, related_name='materias')
    nombre = models.CharField(max_length=100)
    clave = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    creditos = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    orden = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'materias'
        indexes = [
            models.Index(fields=['grado'], name='idx_materia_grado'),
            models.Index(fields=['programa_educativo'], name='idx_materia_programa'),
            models.Index(fields=['activa'], name='idx_materia_activa'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.clave})"


class PeriodoEvaluacion(models.Model):
    """
    Períodos de evaluación dentro de un ciclo escolar.
    """
    ESTATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ACTIVO', 'Activo'),
        ('CERRADO', 'Cerrado'),
    ]

    ciclo_escolar = models.ForeignKey(CicloEscolar, on_delete=models.PROTECT, related_name='periodos_evaluacion')
    programa_educativo = models.ForeignKey(ProgramaEducativo, on_delete=models.PROTECT, related_name='periodos_evaluacion')
    numero_periodo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_inicio_captura = models.DateField(editable=False)
    fecha_fin_captura = models.DateField(editable=False)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'periodos_evaluacion'
        unique_together = ('ciclo_escolar', 'programa_educativo', 'numero_periodo')
        indexes = [
            models.Index(fields=['ciclo_escolar'], name='idx_periodo_ciclo'),
            models.Index(fields=['programa_educativo'], name='idx_periodo_programa'),
            models.Index(fields=['estatus'], name='idx_periodo_estatus'),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.ciclo_escolar}"

    def save(self, *args, **kwargs):
        self.fecha_fin_captura = self.fecha_fin
        self.fecha_inicio_captura = self.fecha_fin - timedelta(days=7)
        super().save(*args, **kwargs)


class Maestro(models.Model):
    """
    Representa a los profesores (extiende el modelo de usuarios).
    """
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, related_name='maestro_perfil')
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.PROTECT, related_name='maestros')
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_contratacion = models.DateField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maestros'
        indexes = [
            models.Index(fields=['usuario'], name='idx_maestro_usuario'),
            models.Index(fields=['nivel_educativo'], name='idx_maestro_nivel'),
            models.Index(fields=['activo'], name='idx_maestro_activo'),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


class AdministradorEscolar(models.Model):
    """
    Administradores por nivel educativo.
    """
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, related_name='admin_escolar_perfil')
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.PROTECT, related_name='administradores_escolares')
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'administradores_escolares'
        indexes = [
            models.Index(fields=['usuario'], name='idx_adminesc_usuario'),
            models.Index(fields=['nivel_educativo'], name='idx_adminesc_nivel'),
            models.Index(fields=['activo'], name='idx_adminesc_activo'),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


class AsignacionMaestro(models.Model):
    """
    Asigna maestros a grupos/materias por ciclo escolar.
    """
    maestro = models.ForeignKey(Maestro, on_delete=models.PROTECT, related_name='asignaciones')
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT, related_name='asignaciones_maestro')
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, related_name='asignaciones')
    ciclo_escolar = models.ForeignKey(CicloEscolar, on_delete=models.PROTECT, related_name='asignaciones_maestro')
    fecha_asignacion = models.DateField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asignaciones_maestro'
        unique_together = ('grupo', 'materia', 'ciclo_escolar')
        indexes = [
            models.Index(fields=['maestro'], name='idx_asignacion_maestro'),
            models.Index(fields=['grupo'], name='idx_asignacion_grupo'),
            models.Index(fields=['materia'], name='idx_asignacion_materia'),
            models.Index(fields=['ciclo_escolar'], name='idx_asignacion_ciclo'),
            models.Index(fields=['activa'], name='idx_asignacion_activa'),
        ]

    def __str__(self):
        return f"{self.maestro} - {self.materia} ({self.grupo})"


class Calificacion(models.Model):
    """
    Calificaciones de estudiantes por período.
    """
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, related_name='calificaciones_periodo')
    asignacion_maestro = models.ForeignKey(AsignacionMaestro, on_delete=models.PROTECT, related_name='calificaciones')
    periodo_evaluacion = models.ForeignKey(PeriodoEvaluacion, on_delete=models.PROTECT, related_name='calificaciones')
    calificacion = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(10.00)])
    puede_modificar = models.BooleanField(default=True)
    fecha_captura = models.DateTimeField(auto_now_add=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)
    capturada_por = models.ForeignKey(Maestro, on_delete=models.PROTECT, related_name='calificaciones_capturadas')
    modificada_por = models.ForeignKey(Maestro, on_delete=models.PROTECT, null=True, blank=True, related_name='calificaciones_modificadas')
    autorizada_por = models.ForeignKey(AdministradorEscolar, on_delete=models.PROTECT, null=True, blank=True, related_name='calificaciones_autorizadas')

    class Meta:
        db_table = 'calificaciones'
        unique_together = ('estudiante', 'asignacion_maestro', 'periodo_evaluacion')
        indexes = [
            models.Index(fields=['estudiante'], name='idx_calif_estudiante'),
            models.Index(fields=['asignacion_maestro'], name='idx_calif_asignacion'),
            models.Index(fields=['periodo_evaluacion'], name='idx_calif_periodo'),
            models.Index(fields=['fecha_captura'], name='idx_calif_captura'),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
             # Al crear primera vez, se bloquea automaticamante
             self.puede_modificar = False
        else:
             # Si ya existe, verificamos cambios
             old_instance = Calificacion.objects.get(pk=self.pk)
             
             # Caso 1: Admin autoriza (False -> True)
             # No hacemos nada, permitimos que se guarde como True
             
             # Caso 2: Maestro modifica calificación (estaba True y cambia valor)
             if old_instance.puede_modificar and self.calificacion != old_instance.calificacion:
                  self.puede_modificar = False
                  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudiante} - {self.calificacion}"


class CalificacionFinal(models.Model):
    """
    Calificación final y estatus por materia por ciclo escolar.
    """
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, related_name='calificaciones_finales')
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, related_name='calificaciones_finales')
    ciclo_escolar = models.ForeignKey(CicloEscolar, on_delete=models.PROTECT, related_name='calificaciones_finales')
    calificaciones_periodos = models.JSONField()
    calificacion_final = models.DecimalField(max_digits=4, decimal_places=2)
    estatus = models.CharField(max_length=2, choices=[('AO', 'Aprobado Ordinario'), ('RP', 'Reprobado')])
    modificacion_manual = models.BooleanField(default=False)
    calificacion_recursamiento = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    fecha_calculo = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'calificaciones_finales'
        unique_together = ('estudiante', 'materia', 'ciclo_escolar')
        indexes = [
            models.Index(fields=['estudiante'], name='idx_calfinal_estudiante'),
            models.Index(fields=['materia'], name='idx_calfinal_materia'),
            models.Index(fields=['ciclo_escolar'], name='idx_calfinal_ciclo'),
            models.Index(fields=['estatus'], name='idx_calfinal_estatus'),
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.materia} - {self.estatus}"


class AutorizacionCambioCalificacion(models.Model):
    """
    Registro de autorizaciones de cambio de calificaciones.
    """
    calificacion = models.ForeignKey(Calificacion, on_delete=models.PROTECT, related_name='autorizaciones')
    autorizado_por = models.ForeignKey(AdministradorEscolar, on_delete=models.PROTECT, related_name='autorizaciones_dadas')
    motivo = models.TextField()
    fecha_autorizacion = models.DateTimeField(auto_now_add=True)
    utilizada = models.BooleanField(default=False)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    valor_anterior = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    valor_nuevo = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'autorizaciones_cambio_calificacion'
        indexes = [
            models.Index(fields=['calificacion'], name='idx_autcalif_calificacion'),
            models.Index(fields=['autorizado_por'], name='idx_autcalif_admin'),
            models.Index(fields=['utilizada'], name='idx_autcalif_utilizada'),
        ]

    def __str__(self):
        return f"Autorización {self.id} - {self.calificacion}"


class ModificacionManualCalificacion(models.Model):
    """
    Historial de modificaciones manuales de calificaciones finales por el administrador.
    """
    calificacion_final = models.ForeignKey(CalificacionFinal, on_delete=models.PROTECT, related_name='modificaciones_manuales')
    calificacion = models.ForeignKey(Calificacion, on_delete=models.PROTECT, related_name='modificaciones_manuales_admin')
    modificado_por = models.ForeignKey(AdministradorEscolar, on_delete=models.PROTECT, related_name='modificaciones_manuales_realizadas')
    valor_anterior = models.DecimalField(max_digits=4, decimal_places=2)
    valor_nuevo = models.DecimalField(max_digits=4, decimal_places=2)
    motivo = models.TextField()
    estatus_anterior = models.CharField(max_length=2)
    estatus_nuevo = models.CharField(max_length=2)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'modificaciones_manuales_calificaciones'
        indexes = [
            models.Index(fields=['calificacion_final'], name='idx_modman_calfinal'),
            models.Index(fields=['calificacion'], name='idx_modman_calif'),
            models.Index(fields=['modificado_por'], name='idx_modman_admin'),
            models.Index(fields=['fecha_modificacion'], name='idx_modman_fecha'),
        ]

    def __str__(self):
        return f"Modificación {self.id} - {self.calificacion_final}"
