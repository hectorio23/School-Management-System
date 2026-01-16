from django.db import models
from estudiantes.models import Estudiante
from datetime import timedelta
from django.utils import timezone

#########################################################
# PAGOS Y ADEUDOS
#########################################################

class ConceptoPago(models.Model):
    """
    Catálogo de conceptos de pago: Colegiatura, Inscripción, Uniforme, etc.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    monto_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Monto base antes de descuentos'
    )
    nivel_educativo = models.CharField(
        max_length=100,
        help_text='Primaria, Secundaria, Preparatoria, Todos'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Concepto de Pago"
        verbose_name_plural = "Conceptos de Pago"
        unique_together = [['nombre', 'nivel_educativo']]
        db_table = 'conceptos_pago'
        indexes = [
            models.Index(fields=['activo'], name='idx_concepto_activo'),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.nivel_educativo}"


class Adeudo(models.Model):
    """
    Adeudos generados por concepto.
    Los recargos se calculan automáticamente.
    UN ADEUDO POR CONCEPTO POR ESTUDIANTE.
    """
    ESTATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('vencido', 'Vencido'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        db_column='estudiante_id'
    )
    concepto = models.ForeignKey(
        ConceptoPago,
        on_delete=models.CASCADE,
        db_column='concepto_id'
    )

    # Montos
    monto_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Monto original del concepto'
    )

    descuento_aplicado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Descuento aplicado por estrato'
    )

    recargo_aplicado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Recargo por mora'
    )

    monto_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='monto_final + recargo_aplicado'
    )

    # Fechas
    fecha_generacion = models.DateField(
        help_text='Fecha en que se generó el adeudo',
        auto_now=True
    )
    fecha_vencimiento = models.DateField(
        help_text='Fecha límite de pago',
        default=timezone.now() + timedelta(days=31)
    )

    # Estado
    estatus = models.CharField(
        max_length=50,
        choices=ESTATUS_CHOICES,
        default='pendiente'
    )

    # Timestamps
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    # fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Adeudo"
        verbose_name_plural = "Adeudos"
        db_table = 'adeudos'
        indexes = [
            models.Index(fields=['estudiante'], name='idx_adeudo_estudiante'),
            models.Index(fields=['concepto'], name='idx_adeudo_concepto'),
            models.Index(fields=['fecha_vencimiento'], name='idx_adeudo_vencimiento'),
            models.Index(fields=['estatus'], name='idx_adeudo_estatus'),
            models.Index(
                fields=['estudiante', 'concepto', 'fecha_generacion'],
                name='idx_adeudo_seguimiento'
            ),
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.concepto} (${self.monto_total})"

    def esta_vencido(self):
        """Verifica si el adeudo está vencido"""
        from django.utils import timezone
        return (
            self.fecha_vencimiento < timezone.now().date() 
            and self.estatus in ['Vencido', 'vencido']
        )

    # def actualizar_estatus(self):
    #     """Actualiza el estatus según el monto pagado"""
    #     if self.monto_pagado >= self.monto_total:
    #         self.estatus = 'pagado'

    #     self.save()


class Pago(models.Model):
    """
    Pagos realizados contra adeudos.
    Un adeudo puede tener múltiples pagos (pagos parciales)
    """
    # 1 pago solo pude pertenecer a 1 solo adeudo, lo quese puede traducir en que
    # cada estudiante puede realizar un solo pago a la vez.
    adeudo = models.OneToOneField(
        Adeudo,
        on_delete=models.CASCADE,
        db_column='adeudo_id'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(
        max_length=100,
        help_text='Efectivo, Tarjeta, Transferencia, Cheque'
    )
    numero_referencia = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Número de referencia bancaria'
    )
    ruta_recibo = models.TextField(
        null=True,
        blank=True,
        help_text='Ruta al comprobante de pago'
    )

    # Metadata
    recibido_por = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Usuario que registró el pago'
    )
    notas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = 'pagos'
        indexes = [
            models.Index(fields=['adeudo'], name='idx_pago_adeudo'),
            models.Index(fields=['fecha_pago'], name='idx_pago_fecha'),
            models.Index(fields=['metodo_pago'], name='idx_pago_metodo'),
        ]

    def __str__(self):
        return f"Pago ${self.monto} - {self.fecha_pago.date()}"

    def save(self, *args, **kwargs):
        """Al guardar un pago, actualiza el adeudo"""
        super().save(*args, **kwargs)
        
        # Actualizar monto_pagado del adeudo
        from django.db.models import Sum
        total_pagado = self.adeudo.pago_set.aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        self.adeudo.monto_pagado = total_pagado
        self.adeudo.actualizar_estatus()
