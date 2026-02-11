from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener email")
        if not role:
            raise ValueError("El usuario debe tener un rol")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, role="administrador", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, role, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = (
        ("estudiante", "Estudiante"),
        ("administrador", "Administrador TI"),
        ("becas_admin", "Administrador de Becas"),
        ("finanzas_admin", "Administrador de Finanzas"),
        ("comedor_admin", "Administrador de Comedor"),
        ("admisiones_admin", "Administrador de Admisiones"),
        ("maestro", "Maestro"),
        ("admin_escolar", "Administrador Escolar"),
        ("bibliotecario", "Administrador de Biblioteca"),
    )

    # Roles que tienen privilegios administrativos
    ADMIN_ROLES = ['administrador', 'becas_admin', 'finanzas_admin', 'comedor_admin', 'admisiones_admin']

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=200)
    role = models.CharField(max_length=20, default="estudiante", choices=ROLE_CHOICES)

    activo = models.BooleanField(default=True)

    """Campos requerido para entrar al login propio de django, se eliminarán en produccion"""
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  

    mfa_code = models.CharField(max_length=6, null=True, blank=True)
    mfa_expires_at = models.DateTimeField(null=True, blank=True)

    def clear_mfa(self):

        if self.role.upper() == "ESTUDIANTE":
            return None

        self.mfa_code = None
        self.mfa_expires_at = None
        self.save(update_fields=["mfa_code", "mfa_expires_at"])

    def is_admin_role(self):
        """Verifica si el usuario tiene algún rol administrativo."""
        return self.role in self.ADMIN_ROLES

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"


class LoginAttempt(models.Model):
    """
    Registro de intentos de inicio de sesión para protección contra fuerza bruta.
    """
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=False)

    class Meta:
        db_table = "login_attempts"
        indexes = [
            models.Index(fields=["email", "timestamp"], name="idx_login_email_time"),
            models.Index(fields=["ip_address", "timestamp"], name="idx_login_ip_time"),
        ]

    def __str__(self):
        status = "EXITOSO" if self.was_successful else "FALLIDO"
        return f"{self.email} - {self.timestamp} - {status}"
