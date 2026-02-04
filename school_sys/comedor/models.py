from django.db import models
from estudiantes.models import Estudiante
import os
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
try:
    from pagos.models import Adeudo, ConceptoPago
except ImportError:
    # Handle circular import if necessary, but preferred at top
    pass


#########################################################
# CAFETERÍA
#########################################################

class Menu(models.Model):
    descripcion = models.CharField(
        max_length=160,
        help_text="Nombre de la comida"
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
        return self.descripcion


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
        help_text='Precio aplicado (se automatiiza al guardar si está vacio)',
        null=True,
        blank=True
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

    def save(self, *args, **kwargs):
        if not self.precio_aplicado:
            self.precio_aplicado = Decimal(os.getenv('COSTO_COMIDA', '10.00'))
        super().save(*args, **kwargs)

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


class AdeudoComedor(models.Model):
    """
    Adeudos generados por consumo en cafetería.
    Adeudos generados por consumo en cafetería.
    Vinculado via OneToOne al modelo principal pagos.Adeudo.
    """
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asistencia = models.ForeignKey(AsistenciaCafeteria, on_delete=models.CASCADE)
    
    # Vinculo fuerte con la tabla contable principal
    adeudo = models.OneToOneField(
        'pagos.Adeudo', 
        on_delete=models.CASCADE,
        null=True, # Null temporalmente para migracion, luego required
        related_name='detalle_comedor'
    )
    
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    
    fecha_generacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    
    # Eliminamos 'pagado' y 'fecha_pago' para evitar redundancia y deuda tecnica.
    # La verdad unica reside en self.adeudo.estatus == 'pagado'
    
    recargo_aplicado = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    monto_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=10.00
    )
    
    class Meta:
        verbose_name = "Adeudo de Comedor"
        verbose_name_plural = "Adeudos de Comedor"
        db_table = "adeudos_comedor"
        indexes = [
            models.Index(fields=['estudiante'], name='idx_adeudo_comedor_est'),
            # idx_adeudo_comedor_pagado eliminado pues el campo ya no existe
        ]

    @property
    def pagado(self):
        if self.adeudo:
            return self.adeudo.estatus == 'pagado'
        return False

    def save(self, *args, **kwargs):
        # 1. Usar monto por defecto desde variable de entorno
        default_amount = Decimal(os.getenv('COSTO_COMIDA', '10.00'))
        self.monto = default_amount

        # 2. Calcular Fecha de Vencimiento (Día 10 del mes siguiente)
        if not self.fecha_vencimiento:
            hoy = timezone.localdate()
            if hoy.month == 12:
                mes_v = 1
                anio_v = hoy.year + 1
            else:
                mes_v = hoy.month + 1
                anio_v = hoy.year
            self.fecha_vencimiento = date(anio_v, mes_v, 10)

        # 3. Verificar si aplicar descuentos (beca + estrato)
        # Si APPLY_TOTAL_DISCOUNT=0, NO se aplican descuentos al comedor
        apply_discount = os.getenv('APPLY_TOTAL_DISCOUNT', '0') == '1'
        
        descuento = Decimal('0.00')
        if apply_discount and self.estudiante:
            # Aplicar descuentos de beca + estrato
            descuento = self.estudiante.get_monto_descuento(self.monto)
        
        monto_con_descuento = max(Decimal('0.00'), self.monto - descuento)

        # 4. Verificar Recargos (Local logic)
        # Usamos self.pagado (property) para checar
        is_paid = self.pagado
        
        if not is_paid and self.fecha_vencimiento < timezone.now().date():
            pct_recargo = Decimal(os.getenv('RECARGO_COMEDOR_PORCENTAJE', '120')) / 100
            self.recargo_aplicado = monto_con_descuento * pct_recargo
        else:
            self.recargo_aplicado = Decimal('0.00')

        # 5. Calcular Total
        self.monto_total = monto_con_descuento + self.recargo_aplicado
        
        # 6. Sincronizar/Crear Adeudo Principal
        # Necesitamos un ConceptoPago para Comedor
        concepto, _ = ConceptoPago.objects.get_or_create(
            nombre="Consumo Cafeteria",
            defaults={
                'descripcion': 'Consumo diario de alimentos',
                'monto_base': self.monto,
                'nivel_educativo': 'Todos',
                'tipo_concepto': 'otro'
            }
        )

        if not self.adeudo:
            # Crear Adeudo Nuevo
            nuevo_adeudo = Adeudo.objects.create(
                estudiante=self.estudiante,
                concepto=concepto,
                monto_base=self.monto,
                descuento_aplicado=descuento,
                monto_total=self.monto_total,
                recargo_aplicado=self.recargo_aplicado,
                fecha_vencimiento=self.fecha_vencimiento,
                generado_automaticamente=True,
                justificacion_manual="Generado desde Comedor"
            )
            self.adeudo = nuevo_adeudo
        else:
            # Actualizar Adeudo Existente
            self.adeudo.monto_total = self.monto_total
            self.adeudo.recargo_aplicado = self.recargo_aplicado
            self.adeudo.descuento_aplicado = descuento
            self.adeudo.fecha_vencimiento = self.fecha_vencimiento
            # Evitar recursion infinita si Adeudo.save() llama logica compleja
            # Usar update directo para evitar recálculos
            Adeudo.objects.filter(pk=self.adeudo.pk).update(
                monto_total=self.monto_total,
                recargo_aplicado=self.recargo_aplicado,
                descuento_aplicado=descuento,
                fecha_vencimiento=self.fecha_vencimiento
            )
        
        super().save(*args, **kwargs)

    def __str__(self):
        status = "PAGADO" if self.pagado else "PENDIENTE"
        return f"{self.estudiante} - ${self.monto_total} ({status})"
