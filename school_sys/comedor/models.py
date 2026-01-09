from django.db import models
from estudiantes.models import Estudiante


#########################################################
# CAFETERÍA
#########################################################

class AsistenciaCafeteria(models.Model):
    """Registro de asistencia a cafetería con precio aplicado"""
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_id'
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

