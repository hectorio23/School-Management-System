from django.db import models
from django.utils import timezone
from datetime import datetime

# --- VERIFICACIÓN DE CORREO ---
class VerificationCode(models.Model):
    """Códigos de verificación para validar correos antes del registro"""
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    # Almacenar datos temporales mientras se verifica
    data_json = models.TextField(null=True, blank=True) 

    def is_valid(self):
        return not self.is_verified and self.expires_at > timezone.now()

    class Meta:
        db_table = 'verification_codes'
        indexes = [
            models.Index(fields=['email', 'code'], name='idx_verification_email_code'),
        ]

# --- CUENTAS DE USUARIOS PARA INSCRIPCION --
class AdmissionUser(models.Model):
    """Aqui es donde se registran los usuarios unicamente para realizar la inscipcion,
    después se eliminarán cumpliendose un intervalo de tiempo definido por el administrador.
        - default: 1 week -> 7 days -> 168 hrs
    """
    folio = models.IntegerField(primary_key=True, unique=True, editable=False)
    email = models.EmailField(max_length=255, unique=True) # Changed max_length and added unique
    password = models.CharField(max_length=128) # Increased length for hashed passwords
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.folio:
            last = AdmissionUser.objects.all().order_by('folio').last()
            if last:
                self.folio = last.folio + 1
            else:
                self.folio = 2000
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        db_table = 'usuarios_aspirantes'
        indexes = [
            models.Index(fields=['folio'], name='idx_aspirante_folio'),
            models.Index(fields=['email'], name='idx_aspirante_email'),
        ]

class AdmissionTutor(models.Model):
    """Almacenaje de tutores"""
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, null=True)
    apellido_materno = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    numero_telefono = models.CharField(max_length=20) 
    
    # Campo extra para CURP del tutor si es necesario en validación
    curp = models.CharField(max_length=18, null=True, blank=True)

    def __str__(self):
        return f"{ self.apellido_paterno } { self.apellido_materno } { self.nombre }"

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"
        db_table = 'tutor_temp'
        indexes = [
            models.Index(
                fields=['apellido_paterno', 'apellido_materno', 'nombre'],
                name='idx_tutoradm_nombre_completo'
            ),
        ]

class Aspirante(models.Model):
    """Informacion COMPLETA del aspirante para las 4 fases"""
    SEXOS = [('M', 'Masculino'), ('F', 'Femenino')]
    STATUS_CHOICES = [
        ('ASPIRANTE', 'Aspirante'),
        ('ACEPTADO', 'Aceptado'),
        ('NO_ACEPTADO', 'No Aceptado'),
    ]
    
    # CONTROL DE PROCESO
    user = models.OneToOneField(AdmissionUser, on_delete=models.CASCADE)
    fase_actual = models.IntegerField(default=1, help_text='1:Datos, 2:Socio, 3:Docs, 4:Pago, 5:Fin')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASPIRANTE')

    # FASE 1: DATOS PERSONALES
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, null=True)
    apellido_materno = models.CharField(max_length=100, null=True)
    curp = models.CharField(max_length=18, unique=True, null=False, blank=False) # Forzado
    fecha_nacimiento = models.DateField(null=True)
    sexo = models.CharField(max_length=1, choices=SEXOS, null=True) # Renombrado
    direccion = models.TextField(null=True)
    telefono = models.CharField(max_length=20, null=True)
    escuela_procedencia = models.CharField(max_length=255, null=True)
    promedio_anterior = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    # FASE 2: ESTUDIO SOCIOECONÓMICO
    ingreso_mensual_familiar = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ocupacion_padre = models.CharField(max_length=100, null=True, blank=True)
    ocupacion_madre = models.CharField(max_length=100, null=True, blank=True)
    tipo_vivienda = models.CharField(max_length=50, null=True, help_text='Propia, Rentada, Prestada')
    miembros_hogar = models.IntegerField(null=True)
    vehiculos = models.IntegerField(default=0, null=True)
    internet_encasa = models.BooleanField(default=False)
    
    # FASE 3: DOCUMENTACIÓN Y LEGAL
    # Archivos del Aspirante
    comprobante_domicilio = models.FileField(upload_to='admissions/documents/domicilio/', null=True, blank=True)
    curp_pdf = models.FileField(upload_to='admissions/documents/curp/', null=True, blank=True)
    acta_nacimiento_estudiante = models.FileField(upload_to='admissions/documents/actas/', null=True, blank=True)
    # Archivos de Tutores (se podrían separar, pero el usuario pidió tabla única de aspirantes con campos extra)
    acta_nacimiento_tutor = models.FileField(upload_to='admissions/documents/actas_tutores/', null=True, blank=True)
    curp_tutor_pdf = models.FileField(upload_to='admissions/documents/curp_tutores/', null=True, blank=True)
    
    # Checks obligatorios
    acta_nacimiento_check = models.BooleanField(default=False)
    curp_check = models.BooleanField(default=False)
    aceptacion_reglamento = models.BooleanField(default=False)
    autorizacion_imagen = models.BooleanField(default=False)

    # FASE 4: PAGO DE INSCRIPCIÓN
    fecha_pago = models.DateTimeField(null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=400)
    metodo_pago = models.CharField(
        max_length=100,
        help_text='Efectivo, Tarjeta, Transferencia, Cheque',
        null=True, blank=True
    )
    numero_referencia = models.CharField(max_length=255, null=True, blank=True)
    ruta_recibo = models.TextField(null=True, blank=True, help_text='Ruta al comprobante (si aplica)')
    pagado_status = models.BooleanField(default=False) # Renombrado de 'status' original para evitar conflicto
    
    # Metadata
    recibido_por = models.CharField(max_length=255, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{ self.user.folio } - { self.apellido_paterno } { self.nombre }"
    
    class Meta:
        verbose_name = "Aspirante"
        verbose_name_plural = "Aspirantes"
        db_table = 'aspirantes'
        indexes = [
            models.Index(fields=['curp'], name='idx_aspirante_curp'),
            models.Index(fields=['fase_actual'], name='idx_aspirante_fase'),
        ]

class AdmissionTutorAspirante(models.Model):
    """
    Relación M:M entre aspirantes y tutores
    """
    aspirante = models.ForeignKey(
        Aspirante, 
        on_delete=models.CASCADE,
        db_column='aspirante_id'
    )
    tutor = models.ForeignKey(
        AdmissionTutor, 
        on_delete=models.CASCADE,
        db_column='tutor_id'
    )
    parentesco = models.CharField(
        max_length=100,
        help_text='Padre, Madre, Abuelo, Tutor Legal, etc.'
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tutor de Aspirante"
        verbose_name_plural = "Aspirantes-Tutores"
        unique_together = [['aspirante', 'tutor']]
        db_table = 'aspirante_tutor'