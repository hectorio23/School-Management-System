import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.files.base import ContentFile
from .utils_security import generate_folio_hash, encrypt_data

# --- MANAGER PARA AdmissionUser ---
class AdmissionUserManager(BaseUserManager):
    """Administrador personalizado para AdmissionUser."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash automático de la contraseña
        user.save(using=self._db)
        return user

# --- VERIFICACIÓN DE CORREO ---
class VerificationCode(models.Model):
    """Códigos de verificación para validar correos electrónicos antes del registro."""
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    data_json = models.TextField(null=True, blank=True) 

    def is_valid(self):
        """Verifica si el código aún es válido (no usado y no expirado)."""
        return not self.is_verified and self.expires_at > timezone.now()

    class Meta:
        db_table = "verification_codes"
        indexes = [
            models.Index(fields=["email", "code"], name="idx_verification_email_code"),
        ]

# --- CUENTAS DE USUARIOS PARA INSCRIPCION --
class AdmissionUser(AbstractBaseUser):
    """
    Usuarios temporales únicamente para realizar el proceso de inscripción.
    Hereda de AbstractBaseUser para manejar autenticación estándar.
    """
    folio = models.IntegerField(primary_key=True, unique=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    @property
    def id(self):
        return self.folio

    # Configuración de Django Auth
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = AdmissionUserManager()

    def save(self, *args, **kwargs):
        """Asigna un folio automático a partir de 2000 si no existe."""
        if not self.folio:
            last = AdmissionUser.objects.all().order_by("folio").last()
            if last:
                self.folio = last.folio + 1
            else:
                self.folio = 2000
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Folio {self.folio} - {self.email}"

    class Meta:
        verbose_name = "Usuario Aspirante"
        verbose_name_plural = "Usuarios Aspirantes"
        db_table = "usuarios_aspirantes"
        indexes = [
            models.Index(fields=["folio"], name="idx_aspirante_folio"),
            models.Index(fields=["email"], name="idx_aspirante_email"),
        ]

# --- RUTAS DE ALMACENAMIENTO HASHED ---

def tutor_upload_path(instance, filename):
    """Genera una ruta hasheada para documentos del tutor basada en su CURP."""
    input_str = instance.curp if instance.curp else str(instance.id)
    tutor_hash = generate_folio_hash(input_str)
    return f"admissions/documents/tutors/{tutor_hash}/{filename}"

def aspirante_upload_path(instance, filename):
    """Genera una ruta hasheada para documentos del aspirante basada en su folio."""
    folio_hash = generate_folio_hash(instance.user.folio)
    return f"admissions/documents/aspirantes/{folio_hash}/{filename}"

# --- MODELOS DE ADMISIÓN ---

class AdmissionTutor(models.Model):
    """Información de contacto y documentos legales del tutor."""
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, null=True)
    apellido_materno = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    numero_telefono = models.CharField(max_length=20) 
    curp = models.CharField(max_length=18, null=True, blank=True)
    
    # Documentos con almacenamiento seguro (Hashed & Encrypted)
    acta_nacimiento = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    curp_pdf = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    
    # Nuevos documentos del tutor
    comprobante_domicilio = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    foto_fachada_domicilio = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    comprobante_ingresos = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    carta_ingresos = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    ine_tutor = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    contrato_arrendamiento_predial = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)
    carta_bajo_protesta = models.FileField(upload_to=tutor_upload_path, max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Encripta archivos del tutor antes de persistirlos en disco."""
        tutor_files = [
            'acta_nacimiento', 'curp_pdf', 'comprobante_domicilio', 'foto_fachada_domicilio',
            'comprobante_ingresos', 'carta_ingresos', 'ine_tutor', 
            'contrato_arrendamiento_predial', 'carta_bajo_protesta'
        ]
        for field_name in tutor_files:
            try:
                file_field = getattr(self, field_name)
                if file_field and hasattr(file_field, 'file') and not getattr(file_field, '_is_already_encrypted', False):
                    if hasattr(file_field.file, 'read'):
                        content = file_field.file.read()
                        if content:
                            encrypted_content = encrypt_data(content)
                            base_name = os.path.basename(file_field.name)
                            new_file = ContentFile(encrypted_content, name=base_name)
                            setattr(self, field_name, new_file)
                            getattr(self, field_name)._is_already_encrypted = True
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombre}"

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"
        db_table = "tutor_temp"
        indexes = [
            models.Index(
                fields=["apellido_paterno", "apellido_materno", "nombre"],
                name="idx_tutoradm_nombre_completo"
            ),
        ]

class Aspirante(models.Model):
    """Información completa del aspirante para las fases del proceso de admisión."""
    SEXOS = [("M", "Masculino"), ("F", "Femenino")]
    STATUS_CHOICES = [
        ("ASPIRANTE", "Aspirante"),
        ("ACEPTADO", "Aceptado"),
        ("NO_ACEPTADO", "No Aceptado"),
        ("RECHAZADO", "Rechazado"),
    ]
    NIVEL_CHOICES = [
        ("PREESCOLAR", "Preescolar"),
        ("PRIMARIA", "Primaria"),
        ("SECUNDARIA", "Secundaria"),
    ]
    
    # Control de Proceso
    user = models.OneToOneField(AdmissionUser, on_delete=models.CASCADE)
    fase_actual = models.IntegerField(default=1, help_text="1:Datos, 2:Socio, 3:Docs, 4:Pago, 5:Fin")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ASPIRANTE")
    nivel_ingreso = models.CharField(max_length=20, choices=NIVEL_CHOICES, null=True, blank=True)

    # FASE 1: Datos Personales
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, null=True)
    apellido_materno = models.CharField(max_length=100, null=True)
    curp = models.CharField(max_length=18, unique=True, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=True)
    sexo = models.CharField(max_length=1, choices=SEXOS, null=True)
    direccion = models.TextField(null=True)
    telefono = models.CharField(max_length=20, null=True)
    escuela_procedencia = models.CharField(max_length=255, null=True)
    promedio_anterior = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    # FASE 2: Estudio Socioeconómico
    ingreso_mensual_familiar = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ocupacion_padre = models.CharField(max_length=100, null=True, blank=True)
    ocupacion_madre = models.CharField(max_length=100, null=True, blank=True)
    tipo_vivienda = models.CharField(max_length=50, null=True, help_text="Propia, Rentada, Prestada")
    miembros_hogar = models.IntegerField(null=True)
    vehiculos = models.IntegerField(default=0, null=True)
    internet_encasa = models.BooleanField(default=False)
    
    # FASE 3: Documentación y Legal (Hashed & Encrypted)
    curp_pdf = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    acta_nacimiento = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    foto_credencial = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    boleta_ciclo_anterior = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    boleta_ciclo_actual = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    
    # Campos que ya no se usan directamente tras la refactorización pero se mantienen para compatibilidad temporal si es necesario
    comprobante_domicilio = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    acta_nacimiento_estudiante = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    acta_nacimiento_tutor = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    curp_tutor_pdf = models.FileField(upload_to=aspirante_upload_path, max_length=255, null=True, blank=True)
    
    acta_nacimiento_check = models.BooleanField(default=False)
    curp_check = models.BooleanField(default=False)
    aceptacion_reglamento = models.BooleanField(default=False)
    autorizacion_imagen = models.BooleanField(default=False)

    # FASE 4: Pago de Inscripción
    fecha_pago = models.DateTimeField(null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=400)
    metodo_pago = models.CharField(max_length=100, null=True, blank=True)
    numero_referencia = models.CharField(max_length=255, null=True, blank=True)
    ruta_recibo = models.TextField(null=True, blank=True)
    pagado_status = models.BooleanField(default=False)
    recibido_por = models.CharField(max_length=255, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    # NUEVOS CAMPOS ADMINISTRATIVOS
    fecha_visita_domiciliaria = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora de la visita domiciliaria")
    fecha_entrevista_psicologia = models.DateField(null=True, blank=True, help_text="Fecha de la entrevista de psicología")
    fecha_examen_pedagogico = models.DateField(null=True, blank=True, help_text="Fecha de aplicación de exámenes pedagógicos")
    comentarios_analisis = models.TextField(null=True, blank=True, help_text="Comentarios del análisis de solicitud")
    comentarios_comite = models.TextField(null=True, blank=True, help_text="Comentarios del comité de admisiones")

    def save(self, *args, **kwargs):
        """Encripta archivos del aspirante antes de persistirlos en disco."""
        files_to_encrypt = [
            'curp_pdf', 'acta_nacimiento', 'foto_credencial', 
            'boleta_ciclo_anterior', 'boleta_ciclo_actual',
            'comprobante_domicilio', 'acta_nacimiento_estudiante', 
            'acta_nacimiento_tutor', 'curp_tutor_pdf'
        ]
        for field_name in files_to_encrypt:
            try:
                file_field = getattr(self, field_name)
                if file_field and hasattr(file_field, 'file') and not getattr(file_field, '_is_already_encrypted', False):
                    if hasattr(file_field.file, 'read'):
                        content = file_field.file.read()
                        if content:
                            encrypted_content = encrypt_data(content)
                            base_name = os.path.basename(file_field.name)
                            new_file = ContentFile(encrypted_content, name=base_name)
                            setattr(self, field_name, new_file)
                            getattr(self, field_name)._is_already_encrypted = True
            except Exception:
                pass
        super().save(*args, **kwargs)

    @property
    def tutores(self):
        """Retorna todos los tutores asociados a este aspirante."""
        return [rel.tutor for rel in AdmissionTutorAspirante.objects.filter(aspirante=self)]

    def __str__(self):
        return f"{self.user.folio} - {self.apellido_paterno} {self.nombre}"
    
    class Meta:
        verbose_name = "Aspirante"
        verbose_name_plural = "Aspirantes"
        db_table = "aspirantes"
        indexes = [
            models.Index(fields=["curp"], name="idx_aspirante_curp"),
            models.Index(fields=["fase_actual"], name="idx_aspirante_fase"),
        ]

class AdmissionTutorAspirante(models.Model):
    """Relación muchos-a-muchos entre aspirantes y sus tutores legales."""
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE, db_column="aspirante_id")
    tutor = models.ForeignKey(AdmissionTutor, on_delete=models.CASCADE, db_column="tutor_id")
    parentesco = models.CharField(max_length=100, help_text="Padre, madre, Abuelo, Tutor Legal, etc.")
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tutor de Aspirante"
        verbose_name_plural = "Aspirantes-Tutores"
        unique_together = [["aspirante", "tutor"]]
        db_table = "aspirante_tutor"