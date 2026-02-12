from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from decimal import Decimal
from users.models import User

#########################################################
# NIVELES Y CICLOS
#########################################################

class NivelEducativo(models.Model):
    """
    Niveles educativos: Preescolar, Primaria, Secundaria.
    Define la estructura macro del colegio.
    """
    nombre = models.CharField(max_length=50, unique=True)
    orden = models.IntegerField(help_text="1=Preescolar, 2=Primaria, 3=Secundaria")
    grados_totales = models.IntegerField(help_text="Cuántos grados tiene este nivel (ej: 3, 6)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nivel Educativo"
        verbose_name_plural = "Niveles Educativos"
        ordering = ['orden']
        db_table = 'niveles_educativos'

    def __str__(self):
        return self.nombre


class CicloEscolar(models.Model):
    """
    Ciclo escolar (ej: 2024-2025).
    Determina qué inscripciones y grupos están activos.
    """
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: 2024-2025")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=False, help_text="Solo un ciclo debe estar activo a la vez")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ciclo Escolar"
        verbose_name_plural = "Ciclos Escolares"
        ordering = ['-fecha_inicio']
        db_table = 'ciclos_escolares'

    def __str__(self):
        estado = "[ACTIVO]" if self.activo else ""
        return f"{self.nombre} {estado}"

    def save(self, *args, **kwargs):
        # Asegurar que solo hay un ciclo activo
        if self.activo:
            CicloEscolar.objects.filter(activo=True).exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)


#########################################################
# GRADOS Y GRUPOS
#########################################################

class Grado(models.Model):
    """Grados académicos del sistema"""
    nombre = models.CharField(max_length=50)  # "1°", "2°", "3°"
    
    # Nuevo campo FK (opcional por ahora para migración)
    nivel_educativo = models.ForeignKey(
        NivelEducativo, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        related_name='grados'
    )
    
    numero_grado = models.IntegerField(
        default=1,
        help_text="Grado relativo al nivel (1, 2, 3...)"
    )
    
    orden_global = models.IntegerField(
        default=0,
        help_text="Orden secuencial absoluto (1=1°Prees, ..., 12=3°Sec)"
    )

    # Deprecated: Se mantendrá mientras se migra a nivel_educativo
    nivel = models.CharField(max_length=100, help_text="DEPRECATED: Usar nivel_educativo")  

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        unique_together = [['nombre', 'nivel']] # Considerar cambiar esto post-migración
        db_table = 'grados'
        ordering = ['orden_global']
        indexes = [
            models.Index(fields=['nombre', 'nivel'], name='idx_grado_nombre_nivel'),
            models.Index(fields=['orden_global'], name='idx_grado_orden_global'),
        ]

    def __str__(self):
        if self.nivel_educativo:
            return f"{self.nombre} {self.nivel_educativo.nombre}"
        return f"{self.nombre} - {self.nivel}"


class Grupo(models.Model):
    """Grupos escolares por ciclo"""
    nombre = models.CharField(max_length=100, help_text="A, B, C")
    
    # Nuevo campo FK (opcional por ahora)
    ciclo_escolar = models.ForeignKey(
        CicloEscolar,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='grupos'
    )
    
    # TODO: Generacion a la que pertenece el estudiante <ciclo escolar de ingreso>
    generacion = models.CharField(
        max_length=50, 
        help_text="DEPRECATED: Usar ciclo_escolar. Ejemplo: 2024-2025"
    )  
    
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    capacidad_maxima = models.IntegerField(default=30)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, db_column='grado_id')

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        # unique_together = [['nombre', 'ciclo_escolar', 'grado']] # Habilitar post-migración
        db_table = 'grupos'
        indexes = [
            models.Index(fields=['grado'], name='idx_grupo_grado'),
            models.Index(fields=['ciclo_escolar'], name='idx_grupo_ciclo'),
        ]

    def __str__(self):
        grado_str = self.grado.nombre if self.grado else "S/G"
        ciclo_str = self.ciclo_escolar.nombre if self.ciclo_escolar else "S/C"
        return f"{grado_str}{self.nombre} ({ciclo_str})"



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

    # Campos migrados desde Aspirante
    curp = models.CharField(
        max_length=18, 
        unique=True, 
        null=True, 
        blank=True,
        validators=[MinLengthValidator(18)],
        help_text="CURP del estudiante"
    )
    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True,
        help_text="Fecha de nacimiento del estudiante"
    )
    sexo = models.CharField(
        max_length=1, 
        choices=[("M", "Masculino"), ("F", "Femenino")], 
        null=True, 
        blank=True
    )
    telefono = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        help_text="Teléfono de contacto predeterminado (del tutor principal)"
    )
    escuela_procedencia = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        help_text="Escuela de procedencia del estudiante"
    )

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
    
    @property
    def grupo_actual(self):
        """Obtiene el grupo del ciclo escolar activo."""
        inscripcion = self.inscripciones.filter(grupo__ciclo_escolar__activo=True).select_related('grupo').first()
        return inscripcion.grupo if inscripcion else None

    @property
    def grado_actual(self):
        """Obtiene el grado del ciclo escolar activo."""
        grupo = self.grupo_actual
        return grupo.grado if grupo else None
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return f"{self.matricula} - {self.nombre_completo}"
    
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

    def get_beca_activa(self):
        """Obtiene la beca activa actual del estudiante, si no ha vencido"""
        beca_estudiante = self.becaestudiante_set.filter(
            activa=True,
            beca__valida=True
        ).select_related('beca').first()
        
        if beca_estudiante and beca_estudiante.beca.fecha_vencimiento < timezone.now().date():
            return None
            
        return beca_estudiante.beca if beca_estudiante else None
    
    def get_porcentaje_descuento_total(self):
        """
        [DEPRECATED] Retorna la suma simple de porcentajes.
        Use get_monto_descuento para cálculos precisos.
        """
        beca = self.get_beca_activa()
        pct_beca = beca.porcentaje if beca else Decimal('0.00')
        
        estrato = self.get_estrato_actual()
        pct_estrato = estrato.porcentaje_descuento if estrato else Decimal('0.00')
        
        return pct_beca + pct_estrato

    def get_monto_descuento(self, monto_base):
        """
        Calcula el monto de descuento secuencial:
        1. Se aplica el % del Estrato al monto_base.
        2. Se aplica el % de la Beca sobre el remanente.
        Retorna el MONTO TOTAL de descuento redondeado a 2 decimales.
        """
        if not monto_base:
            return Decimal('0.00')
            
        monto_base = Decimal(str(monto_base))
        
        # 1. Aplicar Estrato primero
        estrato = self.get_estrato_actual()
        pct_estrato = estrato.porcentaje_descuento if estrato else Decimal('0.00')
        
        descuento_estrato = monto_base * (pct_estrato / Decimal('100.00'))
        monto_estratificado = monto_base - descuento_estrato
        
        # 2. Aplicar Beca sobre lo estratificado
        beca = self.get_beca_activa()
        pct_beca = beca.porcentaje if beca else Decimal('0.00')
        
        descuento_beca = monto_estratificado * (pct_beca / Decimal('100.00'))
        
        return (descuento_estrato + descuento_beca).quantize(Decimal('0.01'))

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        db_table = 'estudiantes'
        indexes = [
            models.Index(fields=['matricula'], name='idx_estudiante_matricula'),
            models.Index(
                fields=['apellido_paterno', 'apellido_materno', 'nombre'],
                name='idx_estudiante_nombre_completo'
            ),
        ]

    def __str__(self):
        return f"{self.matricula} - {self.nombre} {self.apellido_paterno}"

    def get_balance_total(self):

        """Calcula el balance total de adeudos pendientes o parciales"""
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
        return f"{self.estudiante} - {self.estado} ({self.fecha_creacion.date()})"


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
    
    # Snapshot del porcentaje de descuento al momento de la evaluación
    # Este campo mantiene el historial inmutable incluso si el estrato se modifica después
    porcentaje_descuento_snapshot = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Porcentaje de descuento del estrato al momento de la evaluación'
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
        return f"Evaluación {self.estudiante} - {estado}"


#########################################################
# BECAS
#########################################################

class Beca(models.Model):
    """Catálogo de becas disponibles"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Porcentaje de descuento de la beca (0.00 a 100.00)'
    )
    fecha_inicio = models.DateField(
        help_text='Fecha de inicio de vigencia de la beca'
    )
    fecha_vencimiento = models.DateField(
        help_text='Fecha de vencimiento de la beca'
    )
    valida = models.BooleanField(
        default=True,
        help_text='Indica si la beca está vigente. Se cambia a False cuando vence.'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Beca"
        verbose_name_plural = "Becas"
        db_table = 'becas'
        indexes = [
            models.Index(fields=['valida'], name='idx_beca_valida'),
            models.Index(fields=['fecha_vencimiento'], name='idx_beca_vencimiento'),
        ]

    def __str__(self):
        estado = "Vigente" if self.valida else "Vencida"
        return f"{self.nombre} ({self.porcentaje}%) - {estado}"
    
    def verificar_vigencia(self):
        """Verifica y actualiza el estado de vigencia de la beca"""

        if self.fecha_vencimiento < timezone.now().date():
            self.valida = False
            self.save(update_fields=['valida'])
        return self.valida


class BecaEstudiante(models.Model):
    """
    Relación M:M entre Beca y Estudiante con historial.
    En lugar de modificar, se crea un nuevo registro cuando se retira la beca.
    """
    beca = models.ForeignKey(
        Beca,
        on_delete=models.CASCADE,
        db_column='beca_id'
    )
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_matricula'
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_retiro = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha en que se retiró la beca. Null si sigue activa.'
    )
    activa = models.BooleanField(
        default=True,
        help_text='True si la beca sigue asignada al estudiante'
    )
    motivo_retiro = models.TextField(
        null=True,
        blank=True,
        help_text='Motivo por el cual se retiró la beca'
    )
    asignado_por = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Usuario que asignó la beca'
    )

    class Meta:
        verbose_name = "Beca-Estudiante"
        verbose_name_plural = "Becas-Estudiantes"
        db_table = 'becas_estudiantes'
        indexes = [
            models.Index(fields=['beca'], name='idx_becaestudiante_beca'),
            models.Index(fields=['estudiante'], name='idx_becaestudiante_estudiante'),
            models.Index(fields=['activa'], name='idx_becaestudiante_activa'),
        ]

    def __str__(self):
        estado = "Activa" if self.activa else "Retirada"
        return f"{self.estudiante} - {self.beca.nombre} ({estado})"
    
    def retirar_beca(self, motivo=None):
        """Retira la beca del estudiante, creando un registro histórico"""
        self.activa = False
        self.fecha_retiro = timezone.now()
    # ... (métodos existentes)
    
class Inscripcion(models.Model):
    """
    Registro histórico de la inscripción de un alumno en un grado/grupo/ciclo específico.
    Permite tener historial académico completo.
    """
    ESTATUS_INSCRIPCION = [
        ('activo', 'Activo'),
        ('completado', 'Completado (Aprobado)'),
        ('reprobado', 'Reprobado'),
        ('baja_temporal', 'Baja Temporal'),
        ('baja_definitiva', 'Baja Definitiva'),
        ('egresado', 'Egresado de Nivel'),
        ('pendiente_pago', 'Pendiente de Pago/Reinscripción'),
        ('pendiente_asignacion', 'Pagado - Pendiente Asignación Grupo'),
    ]

    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name='inscripciones'
    )
    grupo = models.ForeignKey(
        Grupo, 
        on_delete=models.PROTECT,
        related_name='inscripciones'
    )
    @property
    def ciclo_escolar(self):
        """Acceso al ciclo a través del grupo"""
        return self.grupo.ciclo_escolar if self.grupo else None
    
    estatus = models.CharField(
        max_length=50, 
        choices=ESTATUS_INSCRIPCION, 
        default='activo'
    )
    
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Calificación final o promedio del grado (opcional)
    promedio_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        db_table = 'inscripciones'
        unique_together = [['estudiante', 'grupo']] 
        indexes = [
            models.Index(fields=['estudiante'], name='idx_inscripcion_estudiante'),
            models.Index(fields=['estatus'], name='idx_inscripcion_estatus'),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudiante} - {self.grupo} ({self.estatus})"