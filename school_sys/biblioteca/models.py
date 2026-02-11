from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

class Libro(models.Model):
    """
    Representa un libro en la biblioteca.
    """
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    anio = models.IntegerField(verbose_name="Año")
    genero = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    numero_de_ejemplares = models.PositiveIntegerField(default=1)
    numero_de_ejemplares_prestados = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'biblioteca_libros'
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.titulo

    @property
    def ejemplares_disponibles(self):
        return self.numero_de_ejemplares - self.numero_de_ejemplares_prestados

class UsuarioBiblioteca(models.Model):
    """
    Perfil de usuario para la biblioteca (Estudiantes y Maestros).
    """
    TIPO_USUARIO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('maestro', 'Maestro'),
    ]
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_biblioteca')
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    tipo_de_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    class Meta:
        db_table = 'biblioteca_usuarios'
        verbose_name = 'Usuario de Biblioteca'
        verbose_name_plural = 'Usuarios de Biblioteca'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_de_usuario})"

class Prestamo(models.Model):
    """
    Registro de préstamos de libros.
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ]
    
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamos')
    usuario = models.ForeignKey(UsuarioBiblioteca, on_delete=models.PROTECT, related_name='prestamos')
    fecha_de_prestamo = models.DateField(default=timezone.now)
    fecha_de_devolucion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_real_devolucion = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'biblioteca_prestamos'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.nombre}"

class Multa(models.Model):
    """
    Multas generadas por retrasos en devoluciones.
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
    ]
    
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE, related_name='multa')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    fecha_de_pago = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        db_table = 'biblioteca_multas'
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'

    def __str__(self):
        return f"Multa de {self.monto} - {self.prestamo.usuario.nombre}"
