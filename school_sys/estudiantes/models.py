from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

#########################################################
# GRADOS Y GRUPOS
#########################################################

class Grado(models.Model):
    """Grados académicos del sistema"""
    nombre = models.CharField(max_length=50)  # "1°", "2°", "3°"
    nivel = models.CharField(max_length=100)  # Primaria, Secundaria, Preparatoria

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        unique_together = [['nombre', 'nivel']]
        db_table = 'grados'
        indexes = [
            models.Index(fields=['nombre', 'nivel'], name='idx_grado_nombre_nivel'),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.nivel}"


class Grupo(models.Model):
    """Grupos escolares por ciclo"""
    nombre = models.CharField(max_length=100)
    generacion = models.CharField(max_length=50)  # Ciclo escolar: 2024-2025
    descripcion = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, db_column='grado_id')

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        unique_together = [['nombre', 'generacion', 'grado']]
        db_table = 'grupos'
        indexes = [
            models.Index(fields=['grado'], name='idx_grupo_grado'),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.generacion}"


#########################################################
# ESTUDIANTES
#########################################################

class Estudiante(models.Model):
    """
    Datos principales de estudiantes.
    NO contiene estado ni estrato actual (ver tablas de historial)
    """
    matricula = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    direccion = models.TextField()
    grupo = models.ForeignKey(
        Grupo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='grupo_id'
    )

    # Credenciales para sistema
    nombre_usuario = models.CharField(
        max_length=255, 
        unique=True, 
        null=True, 
        blank=True
    )
    hash_contrasena = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(10, message='La contraseña debe tener al menos 10 caracteres')],
        null=False,
        blank=False
    )
    digest_llave = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text='Hash adicional para autenticación'
    )

    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        db_table = 'estudiantes'
        indexes = [
            models.Index(fields=['matricula'], name='idx_estudiante_matricula'),
            models.Index(fields=['nombre_usuario'], name='idx_estudiante_usuario'),
            models.Index(fields=['grupo'], name='idx_estudiante_grupo'),
            models.Index(
                fields=['apellido_paterno', 'apellido_materno', 'nombre'],
                name='idx_estudiante_nombre_completo'
            ),
        ]

    def __str__(self):
        return f"{self.matricula} - {self.nombre} {self.apellido_paterno}"

    def get_estado_actual(self):
        """Obtiene el estado actual del estudiante desde el historial"""
        ultimo_estado = self.historialestadosestudiante_set.order_by('-fecha_efectiva').first()
        return ultimo_estado.estado if ultimo_estado else None

    def get_estrato_actual(self):
        """Obtiene el estrato actual del estudiante desde el historial"""
        ultimo_estrato = self.historialestratoestudiante_set.order_by('-fecha_efectiva').first()
        return ultimo_estrato.estrato if ultimo_estrato else None

    def get_balance_total(self):
        """Calcula el balance total pendiente"""
        from django.db.models import Sum, F
        resultado = self.adeudo_set.filter(
            estatus__in=['pendiente', 'parcial']
        ).aggregate(
            balance=Sum(F('monto_total') - F('monto_pagado'))
        )
        return resultado['balance'] or 0


#########################################################
# TUTORES
#########################################################

class Tutor(models.Model):
    """Tutores o padres de familia"""
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Campos para control de actualización por estudiantes
    ultima_actualizacion = models.DateTimeField(null=True, blank=True)
    actualizado_por_estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tutores_actualizados',
        db_column='actualizado_por_estudiante_id'
    )

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"
        db_table = 'tutores'
        indexes = [
            models.Index(fields=['correo'], name='idx_tutor_correo'),
            models.Index(fields=['telefono'], name='idx_tutor_telefono'),
            models.Index(fields=['ultima_actualizacion'], name='idx_tutor_ultima_actualizacion'),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    def count_estudiantes(self):
        """Cuenta cuántos estudiantes activos tiene este tutor"""
        return self.estudiantetutor_set.filter(activo=True).count()


class EstudianteTutor(models.Model):
    """
    Relación M:M entre estudiantes y tutores con atributos adicionales
    """
    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE,
        db_column='estudiante_id'
    )
    tutor = models.ForeignKey(
        Tutor, 
        on_delete=models.CASCADE,
        db_column='tutor_id'
    )
    parentesco = models.CharField(
        max_length=100,
        help_text='Padre, Madre, Abuelo, Tutor Legal, etc.'
    )
    responsable_pagos = models.BooleanField(default=False)
    recibe_notificaciones = models.BooleanField(default=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(
        default=True,
        help_text='Para dar de baja sin eliminar'
    )

    class Meta:
        verbose_name = "Estudiante-Tutor"
        verbose_name_plural = "Estudiantes-Tutores"
        unique_together = [['estudiante', 'tutor']]
        db_table = 'estudiantes_tutores'
        indexes = [
            models.Index(fields=['estudiante'], name='idx_estudiantetutor_estudiante'),
            models.Index(fields=['tutor'], name='idx_estudiantetutor_tutor'),
            models.Index(fields=['responsable_pagos'], name='idx_responsable_pagos'),
        ]

    def __str__(self):
        return f"{self.estudiante} -> {self.tutor} ({self.parentesco})"


#########################################################
# ESTADOS DEL ESTUDIANTE (TEMPORAL)
#########################################################

class EstadoEstudiante(models.Model):
    """Catálogo de estados posibles del estudiante"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    es_estado_activo = models.BooleanField(
        default=True,
        help_text='Activo, Baja temporal, Baja definitiva, Egresado'
    )

    class Meta:
        verbose_name = "Estado de Estudiante"
        verbose_name_plural = "Estados de Estudiante"
        db_table = 'estados_estudiante'

    def __str__(self):
        return self.nombre


class HistorialEstadosEstudiante(models.Model):
    """
    Historial temporal de estados.
    El estado actual es el último registro por fecha_efectiva
    """
    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE,
        db_column='estudiante_id'
    )
    estado = models.ForeignKey(
        EstadoEstudiante, 
        on_delete=models.CASCADE,
        db_column='estado_id'
    )
    fecha_efectiva = models.DateTimeField(
        help_text='Fecha en que entra en vigor el estado'
    )
    justificacion = models.TextField(null=True, blank=True)
    creado_por = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Usuario que realizó el cambio'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Estado"
        verbose_name_plural = "Historial de Estados"
        db_table = 'historial_estados_estudiante'
        ordering = ['-fecha_efectiva']
        indexes = [
            models.Index(fields=['estudiante'], name='idx_historialestado_estudiante'),
            models.Index(fields=['estado'], name='idx_historialestado_estado'),
            models.Index(fields=['fecha_efectiva'], name='idx_historialestado_fecha'),
            models.Index(
                fields=['estudiante', 'fecha_efectiva'],
                name='idx_estudiante_estado_temporal'
            ),
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.estado} ({self.fecha_efectiva.date()})"


#########################################################
# ESTRATOS SOCIOECONÓMICOS (TEMPORAL)
#########################################################

class Estrato(models.Model):
    """Catálogo de estratos socioeconómicos con descuentos asociados"""
    nombre = models.CharField(
        max_length=10,
        unique=True,
        help_text='A, B, C, D, etc.'
    )
    descripcion = models.TextField()
    porcentaje_descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Porcentaje de descuento: 0.00 a 100.00'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Estrato"
        verbose_name_plural = "Estratos"
        db_table = 'estratos'
        indexes = [
            models.Index(fields=['activo'], name='idx_estrato_activo'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje_descuento}%)"


class HistorialEstratoEstudiante(models.Model):
    """
    Historial temporal de estratos.
    El estrato actual es el último registro por fecha_efectiva
    """
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_id'
    )
    estrato = models.ForeignKey(
        Estrato,
        on_delete=models.CASCADE,
        db_column='estrato_id'
    )
    fecha_efectiva = models.DateTimeField(
        help_text='Fecha en que entra en vigor el estrato'
    )
    comentarios = models.TextField(null=True, blank=True)
    creado_por = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Estrato"
        verbose_name_plural = "Historial de Estratos"
        db_table = 'historial_estratos_estudiante'
        ordering = ['-fecha_efectiva']
        indexes = [
            models.Index(fields=['estudiante'], name='idx_his_es'),
            models.Index(fields=['estrato'], name='idx_historialestrato_estrato'),
            models.Index(fields=['fecha_efectiva'], name='idx_historialestrato_fecha'),
            models.Index(
                fields=['estudiante', 'fecha_efectiva'],
                name='idx_est_es_temp'
            ),
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.estrato} ({self.fecha_efectiva.date()})"


class EvaluacionSocioeconomica(models.Model):
    """
    Evaluaciones socioeconómicas para determinar estrato.
    Independiente del historial de asignación
    """
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_id'
    )
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    # Datos económicos
    ingreso_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_vivienda = models.CharField(
        max_length=255,
        help_text='Propia, Rentada, Familiar, etc.'
    )
    miembros_hogar = models.IntegerField(
        help_text='Número de personas en el hogar'
    )

    # Resultado de la evaluación
    estrato_sugerido = models.ForeignKey(
        Estrato,
        on_delete=models.CASCADE,
        db_column='estrato_sugerido_id'
    )
    documentos_json = models.TextField(
        help_text='JSON con URLs/paths de documentos probatorios'
    )

    # Metadata
    evaluado_por = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Usuario que realizó la evaluación'
    )
    aprobado = models.BooleanField(
        null=True,
        blank=True,
        help_text='null=pendiente, true=aprobado, false=rechazado'
    )
    aprobado_por = models.CharField(max_length=255, null=True, blank=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Evaluación Socioeconómica"
        verbose_name_plural = "Evaluaciones Socioeconómicas"
        db_table = 'evaluaciones_socioeconomicas'
        indexes = [
            models.Index(fields=['estudiante'], name='idx_evalsocio_estudiante'),
            models.Index(fields=['estrato_sugerido'], name='idx_evalsocio_estrato'),
            models.Index(fields=['fecha_evaluacion'], name='idx_evalsocio_fecha'),
            models.Index(fields=['aprobado'], name='idx_evalsocio_aprobado'),
        ]

    def __str__(self):
        estado = "Aprobada" if self.aprobado else "Pendiente" if self.aprobado is None else "Rechazada"
        return f"[+] Evaluación {self.estudiante} - {estado}"