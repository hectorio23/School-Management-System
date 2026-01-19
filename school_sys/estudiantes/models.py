from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from users.models import User

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
    Datos académicos SOLO de estudiantes.
    Extiende Usuario con información académica.
    """
    # Relación 1:1 con Usuario
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'estudiante'},  # Filtra solo usuarios con rol estudiante
        related_name='perfil_estudiante'
    )
    
    matricula = models.IntegerField(
        primary_key=True,
    )
    
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    direccion = models.TextField()

    updateable = models.BooleanField(default=True)
    porcentaje_beca = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        help_text="Porcentaje de beca asignado (0.00 a 100.00)"
    )
    
    # alergias para comedor
    alergias_alimentarias = models.TextField(
        null=True,
        blank=True,
        help_text='Alergias alimentarias del estudiante'
    )
    
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='grupo_id'
    )
    
    def __str__(self):
        return f"{self.matricula} - {self.nombre} {self.apellido_paterno}"
    
    def save(self, *args, **kwargs):
        # Autogenerar matrícula solo para nuevos estudiantes
        if not self.matricula:
            last_student = Estudiante.objects.order_by('-matricula').first()
            self.matricula = (last_student.matricula + 1) if last_student else 1000
        super().save(*args, **kwargs)
    

    def get_estado_actual(self):
        """Obtiene el estado actual del estudiante desde el historial"""
        ultimo_estado = self.historialestadosestudiante_set.order_by('-fecha_creacion').first()
        return ultimo_estado.estado if ultimo_estado else None


    def get_estrato_actual(self):
        """Obtiene el estrato actual desde la evaluación más reciente aprobada"""
        evaluacion_actual = self.evaluacionsocioeconomica_set.filter(
            aprobado=True,
            estrato__isnull=False
        ).order_by('-fecha_evaluacion').first()
        
        return evaluacion_actual.estrato if evaluacion_actual else None
    
    def get_evaluacion_actual(self):
        """Obtiene la evaluación socioeconómica más reciente"""
        return self.evaluacionsocioeconomica_set.order_by('-fecha_evaluacion').first()
    
    def get_historial_estratos(self):
        """Obtiene el historial de estratos desde las evaluaciones aprobadas"""
        return self.evaluacionsocioeconomica_set.filter(
            aprobado=True,
            estrato__isnull=False
        ).order_by('-fecha_evaluacion').values(
            'estrato__nombre',
            'estrato__porcentaje_descuento',
            'fecha_evaluacion',
            'justificacion_estrato'
        )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        db_table = 'estudiantes'
        indexes = [
            models.Index(fields=['matricula'], name='idx_estudiante_matricula'),
            models.Index(fields=['grupo'], name='idx_estudiante_grupo'),
            models.Index(
                fields=['apellido_paterno', 'apellido_materno', 'nombre'],
                name='idx_estudiante_nombre_completo'
            ),
        ]

    def __str__(self):
        return f"{self.matricula} - {self.nombre} {self.apellido_paterno}"


    def get_balance_total(self):
        """Calcula el balance total pendiente"""
        from django.db.models import Sum, F
        
        resultado = self.adeudo_set.filter(
            estatus__in=['pendiente', 'parcial']
        ).aggregate(
            balance=Sum(F('monto_total'))
        )
        return resultado['balance'] or 0
    
    def check_password(self, raw_password):
        """Verifica la contraseña"""
        return raw_password == self.contrasena
        


#########################################################
# TUTORES
#########################################################

class Tutor(models.Model):
    """Tutores o padres de familia"""
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    telefono = models.CharField(max_length=17) # <+52 449 458 93 45> Los telefonos se almacenarán de esta forma <17 caracteres>
    correo = models.EmailField(null=False, editable=True, max_length=40) # correo obligatorio

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"
        db_table = 'tutores'
        indexes = [
            models.Index(fields=['correo'], name='idx_tutor_correo'),
            models.Index(fields=['telefono'], name='idx_tutor_telefono'),
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
        db_column='estudiante_matricula'
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
        db_column='estudiante_matricula'
    )
    estado = models.ForeignKey(
        EstadoEstudiante, 
        on_delete=models.CASCADE,
        db_column='estado_id'
    )
    justificacion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # fecha de baja
    fecha_baja = models.DateField(
        null=True,
        blank=True,
        help_text='Fecha efectiva de la baja'
    )
    
    # temporal o definitiva
    es_baja_temporal = models.BooleanField(
        null=True,
        blank=True,
        help_text='True=temporal, False=definitiva, null=no es baja'
    )

    class Meta:
        verbose_name = "Historial de Estado"
        verbose_name_plural = "Historial de Estados"
        db_table = 'historial_estados_estudiante'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estudiante'], name='idx_historialestado_estudiante'),
            models.Index(fields=['estado'], name='idx_historialestado_estado'),
        ]

    def __str__(self):
        return f"[+] - {self.estudiante} - {self.estado} ({self.fecha_creacion.date()})"


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
    
    # color para dashboards
    color = models.CharField(
        max_length=7,
        default='#6B7280',
        help_text='Color hex para dashboards ej: #FF5733'
    )
    
    # rangos de ingreso para clasificar
    ingreso_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Ingreso mensual mínimo para este estrato'
    )
    ingreso_maximo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Ingreso mensual máximo para este estrato'
    )

    class Meta:
        verbose_name = "Estrato"
        verbose_name_plural = "Estratos"
        db_table = 'estratos'
        indexes = [
            models.Index(fields=['activo'], name='idx_estrato_activo'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje_descuento}%)"


class EvaluacionSocioeconomica(models.Model):
    """
    Evaluaciones socioeconómicas para determinar estrato.
    Independiente del historial de asignación
    """
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_matricula'
    )

    estrato = models.ForeignKey(
        Estrato,
        on_delete=models.PROTECT,  # No permitir eliminar estratos en uso
        db_column='estrato_id',
        null=True,  # Null mientras está pendiente de aprobación
        blank=True
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

    documentos_json = models.TextField(
        help_text='JSON con URLs/paths de documentos probatorios'
    )

    aprobado = models.BooleanField(
        null=True,
        blank=True,
        help_text='null=pendiente, true=aprobado, false=rechazado'
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    # comentarios de la comision
    comentarios_comision = models.TextField(
        null=True,
        blank=True,
        help_text='Comentarios de la comisión al aprobar/rechazar'
    )
    
    # estrato sugerido automaticamente
    estrato_sugerido = models.ForeignKey(
        Estrato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluaciones_sugeridas',
        help_text='Estrato calculado automáticamente por el sistema'
    )
    
    # si es reconsideracion
    es_reconsideracion = models.BooleanField(
        default=False,
        help_text='True si es solicitud de reconsideración con nueva documentación'
    )
    
    # requiere aprobacion especial (cambios grandes de estrato)
    requiere_aprobacion_especial = models.BooleanField(
        default=False,
        help_text='True si el cambio de estrato es mayor a 2 niveles'
    )
    
    # para revalidacion anual
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
        help_text='Fecha límite para revalidación anual'
    )
    
    # si se notifico
    notificacion_enviada = models.BooleanField(
        default=False,
        help_text='True si ya se notificó al padre/tutor'
    )
    
    # justificacion del estrato
    justificacion_estrato = models.TextField(
        null=True,
        blank=True,
        help_text='Explicación de por qué se asignó este estrato'
    )



    class Meta:
        verbose_name = "Evaluación Socioeconómica"
        verbose_name_plural = "Evaluaciones Socioeconómicas"
        db_table = 'evaluaciones_socioeconomicas'
        indexes = [
            models.Index(fields=['estudiante'], name='idx_evalsocio_estudiante'),
            models.Index(fields=['fecha_evaluacion'], name='idx_evalsocio_fecha'),
            models.Index(fields=['aprobado'], name='idx_evalsocio_aprobado'),
        ]

    def __str__(self):
        estado = "Aprobada" if self.aprobado else "Pendiente" if self.aprobado is None else "Rechazada"
        return f"[+] Evaluación {self.estudiante} - {estado}"