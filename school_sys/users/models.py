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
        ("administrador", "Administrador"),
        ("contador", "Contador"),
        ("cafeteria", "Cafetería"),
    )

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    activo = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Para usar admin
    is_superuser = models.BooleanField(default=False)  # Solo si lo necesitas

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
