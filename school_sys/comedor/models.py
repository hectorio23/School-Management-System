from django.db import models
from estudiantes.models import Estudiante


#########################################################
# CAFETERÍA
#########################################################

class Menu(models.Model):
    descripcion = models.CharField(
        max_length=160,
        help_text="Nombre de la comida"
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Precio'
    )

    desactivar = models.BooleanField(
        default=False,
        help_text="Al desactivar este elemento del menu, ya no saldrá más"
    )
    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menú"
        db_table = 'Menu'

    def __str__(self):
        return f"{ self.descripcion } -> { self.precio }"


class AsistenciaCafeteria(models.Model):
    """Registro de asistencia a cafetería con precio aplicado"""
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_id'
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        db_column='menu_id',
        null=True
    )

    fecha_asistencia = models.DateField()
    tipo_comida = models.CharField(
        max_length=100,
        help_text='Desayuno, Comida, Cena'
    )
    precio_aplicado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Precio aplicado con descuento ya calculado'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asistencia de Cafetería"
        verbose_name_plural = "Asistencias de Cafetería"
        unique_together = [['estudiante', 'fecha_asistencia', 'tipo_comida']]
        db_table = 'asistencia_cafeteria'
        indexes = [
            models.Index(fields=['estudiante'], name='idx_cafeteria_estudiante'),
            models.Index(fields=['fecha_asistencia'], name='idx_cafeteria_fecha'),
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.fecha_asistencia} ({self.tipo_comida})"


class MenuSemanal(models.Model):
    """menus semanales en PDF"""
    semana_inicio = models.DateField(
        help_text='Fecha de inicio de la semana'
    )
    semana_fin = models.DateField(
        help_text='Fecha de fin de la semana'
    )
    archivo_pdf = models.FileField(
        upload_to='menus/',
        help_text='Archivo PDF del menu'
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Descripcion breve del menu'
    )
    activo = models.BooleanField(default=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Menu Semanal"
        verbose_name_plural = "Menus Semanales"
        db_table = 'menus_semanales'
        ordering = ['-semana_inicio']
    
    def __str__(self):
        return f"Menu {self.semana_inicio} - {self.semana_fin}"
