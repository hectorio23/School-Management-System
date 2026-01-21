from django.db import models

# --- CUENTAS DE USUARIOS PARA INSCRIPCION --
class AdmissionUser(models.Model):
    """Aqui es donde se registran los usuarios unicamente para realizar la inscipcion,
    después se eliminarán cumpliendose un intervalo de tiempo definido por el administrador.
        - default: 1 week -> 7 days -> 168 hrs
    """
    folio = models.IntegerField(primary_key=True, default=2000, unique=True)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        db_table = 'usuarios_aspirantes'
        indexes = [
            models.Index(fields=['folio'], name='idx_aspirante_folio'),
        ]


class AdmissionTutor(models.Model):
    """Almacenaje de tutores"""
    nombre = models.CharField(max_length=15)
    apellido_paterno = models.CharField(max_length=20, null=True)
    apellido_materno = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    numero_telefono = models.CharField(max_length=15) 

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
    """Informacion de los aspirantes"""
    user = models.OneToOneField(AdmissionUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=15)
    apellido_paterno = models.CharField(max_length=20, null=True)
    apellido_materno = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{ self.user.folio } - { self.apellido_paterno } { self.apellido_materno } { self.nombre }"

    
    class Meta:
        verbose_name = "Aspirante"
        verbose_name_plural = "Aspirantes"
        db_table = 'aspirantes'
        indexes = [
            models.Index(
                fields=['apellido_paterno', 'apellido_materno', 'nombre'],
                name='idx_aspirante_nombre_completo'
            ),
        ]



class AdmissionTutorAspirante(models.Model):
    """
    Relación M:M entre aspirantes y tutores
    """
    aspirante = models.ForeignKey(
        Aspirante, 
        on_delete=models.CASCADE,
        db_column='aspirante_folio'
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
        verbose_name = "Tutor"
        verbose_name_plural = "Aspirantes-Tutores"
        unique_together = [['aspirante', 'tutor']]
        db_table = 'aspirante_tutor'
        indexes = [
            models.Index(fields=['aspirante'], name='idx_aspirantetutor'),
            models.Index(fields=['tutor'], name='idx_tutoraspirante'),
        ]

    def __str__(self):
        return f"{self.aspirante} -> {self.tutor} ({self.parentesco})"