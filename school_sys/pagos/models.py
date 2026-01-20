from django.db import models
from estudiantes.models import Estudiante
from datetime import timedelta
from django.utils import timezone

#########################################################
# CONFIGURACION DE PAGOS
#########################################################

class ConfiguracionPago(models.Model):
    """configuracion global de pagos"""
    dia_inicio_ordinario = models.IntegerField(
        default=1,
        help_text='Dia del mes donde inicia periodo ordinario'
    )
    dia_fin_ordinario = models.IntegerField(
        default=10,
        help_text='Dia del mes donde termina periodo ordinario'
    )
    porcentaje_recargo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text='Porcentaje de recargo por mora (ej: 10.00)'
    )
    monto_fijo_recargo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=125.00,
        help_text='Monto fijo adicional por recargo'
    )
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Configuracion de Pago"
        verbose_name_plural = "Configuraciones de Pago"
        db_table = 'configuracion_pago'
    
    def __str__(self):
        return f"Config: dia {self.dia_inicio_ordinario}-{self.dia_fin_ordinario}, recargo {self.porcentaje_recargo}%"


class DiaNoHabil(models.Model):
    """dias festivos"""
    fecha = models.DateField(unique=True)
    descripcion = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Dia No Habil"
        verbose_name_plural = "Dias No Habiles"
        db_table = 'dias_no_habiles'
        ordering = ['fecha']
    
    def __str__(self):
        return f"{self.fecha} - {self.descripcion}"


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
    
    monto_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Monto acumulado pagado'
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
    
    # mes correspondiente
    mes_correspondiente = models.DateField(
        null=True,
        blank=True,
        help_text='Primer dia del mes al que corresponde (ej: 2024-01-01)'
    )
    
    # exencion de recargos
    recargo_exento = models.BooleanField(
        default=False,
        help_text='True si el recargo fue exentado'
    )
    justificacion_exencion = models.TextField(
        null=True,
        blank=True,
        help_text='Justificacion de la exencion del recargo'
    )
    
    # automatico o manual
    generado_automaticamente = models.BooleanField(
        default=True,
        help_text='True si fue generado por el sistema'
    )
    justificacion_manual = models.TextField(
        null=True,
        blank=True,
        help_text='Justificacion si fue creado manualmente'
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

    def save(self, *args, **kwargs):
        from decimal import Decimal
        from django.utils import timezone
        import datetime

        # 1. Calcular Fecha de Vencimiento por defecto (día 10 del mes siguiente si no existe)
        if not self.fecha_vencimiento:
            hoy = timezone.localdate()
            mes_siguiente = hoy.month + 1 if hoy.month < 12 else 1
            anio_siguiente = hoy.year if hoy.month < 12 else hoy.year + 1
            try:
                self.fecha_vencimiento = datetime.date(anio_siguiente, mes_siguiente, 10)
            except ValueError:
                # Caso raro, fallback al 28
                self.fecha_vencimiento = datetime.date(anio_siguiente, mes_siguiente, 28)

        # 2. Asegurar Monto Base
        if (self.monto_base is None or self.monto_base == 0) and self.concepto:
             self.monto_base = self.concepto.monto_base
        
        if self.monto_base is None:
             self.monto_base = Decimal('0.00')

        # 3. Calcular Descuentos (solo si es nuevo o se solicita recalcular)
        if self.pk is None and self.estudiante:
            porcentaje_total = self.estudiante.get_porcentaje_descuento_total()
            if porcentaje_total > 0:
                self.descuento_aplicado = self.monto_base * (porcentaje_total / Decimal('100.00'))
                print(self.descuento_aplicado)
            else:
                self.descuento_aplicado = Decimal('0.00')
             
        monto_con_descuento = self.monto_base - self.descuento_aplicado
        if monto_con_descuento < 0:
            monto_con_descuento = Decimal('0.00')

        # 4. Verificar Recargos Automáticos
        # Regla: Si la fecha actual > fecha_vencimiento, aplicar recargo
        hoy = timezone.localdate()
        
        # Aseguramos que fecha_vencimiento sea date para comparar
        vencimiento = self.fecha_vencimiento
        if isinstance(vencimiento, datetime.datetime):
            vencimiento = vencimiento.date()
            
        if vencimiento and hoy > vencimiento and self.estatus in ['pendiente', 'parcial']:
            if not self.recargo_exento:
                porcentaje_recargo = Decimal('0.10') # 10%
                monto_fijo_recargo = Decimal('125.00')
                
                recargo_calculado = (monto_con_descuento * porcentaje_recargo) + monto_fijo_recargo
                self.recargo_aplicado = recargo_calculado
        
        # Si no está vencido o se pagó, no necesariamente quitamos el recargo histórico, 
        # pero si se desea dinámico:
        # else:
        #    self.recargo_aplicado = Decimal('0.00') 
        # Mantenemos el recargo si ya se aplicó para historial, o lo recalculamos siempre?
        # "al pasar esa fecha el sistema AUTOMATICAMENTE debe de aplicar recargo"
        # Asumimos que si se paga tarde, el recargo se mantiene.

        # 5. Calcular Monto Final
        self.monto_total = monto_con_descuento + self.recargo_aplicado

        # 6. Actualizar Estatus
        if self.monto_pagado >= self.monto_total and self.monto_total > 0:
            self.estatus = 'pagado'
        elif self.monto_pagado > 0:
            self.estatus = 'parcial'
        elif self.esta_vencido():
             self.estatus = 'vencido'
        
        super().save(*args, **kwargs)

    def esta_vencido(self):
        """Verifica si el adeudo está vencido"""
        from django.utils import timezone
        import datetime
        
        if not self.fecha_vencimiento:
            return False
            
        vencimiento = self.fecha_vencimiento
        if isinstance(vencimiento, datetime.datetime):
            vencimiento = vencimiento.date()
            
        return (
            vencimiento < timezone.now().date() 
            and self.estatus not in ['pagado', 'cancelado']
        )

    def actualizar_estatus(self):
        """Actualiza el estatus y recalcula montos al recibir un pago"""
        self.save()


class Pago(models.Model):
    """
    Pagos realizados contra adeudos.
    Un adeudo puede tener múltiples pagos (pagos parciales)
    """
    # 1 pago solo pude pertenecer a 1 solo adeudo, lo quese puede traducir en que
    # cada estudiante puede realizar un solo pago a la vez.
    adeudo = models.ForeignKey(
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
