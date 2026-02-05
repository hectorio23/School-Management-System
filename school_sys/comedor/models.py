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

    adeudo = models.OneToOneField(
        'pagos.Adeudo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asistencia_comedor'
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
        # 1. Precio por defecto
        if not self.precio_aplicado:
            self.precio_aplicado = Decimal(os.getenv('COSTO_COMIDA', '10.00'))
        
        super().save(*args, **kwargs)

        # 2. Generar Adeudo Automático si no existe
        if not self.adeudo:
            # Calcular Fecha de Vencimiento (Día 10 del mes siguiente)
            hoy = timezone.localdate()
            if hoy.month == 12:
                mes_v = 1
                anio_v = hoy.year + 1
            else:
                mes_v = hoy.month + 1
                anio_v = hoy.year
            fecha_vencimiento = date(anio_v, mes_v, 10)

            # Verificar descuentos
            apply_discount = os.getenv('APPLY_TOTAL_DISCOUNT', '0') == '1'
            descuento = Decimal('0.00')
            if apply_discount:
                descuento = self.estudiante.get_monto_descuento(self.precio_aplicado)
            
            monto_total = max(Decimal('0.00'), self.precio_aplicado - descuento)

            # Concepto Comedor
            concepto, _ = ConceptoPago.objects.get_or_create(
                nombre="Consumo Cafeteria",
                defaults={
                    'descripcion': 'Consumo diario de alimentos',
                    'monto_base': self.precio_aplicado,
                    'nivel_educativo': 'Todos',
                    'tipo_concepto': 'otro'
                }
            )

            # Crear Adeudo Principal
            nuevo_adeudo = Adeudo.objects.create(
                estudiante=self.estudiante,
                concepto=concepto,
                tipo_adeudo='COMEDOR',
                monto_base=self.precio_aplicado,
                descuento_aplicado=descuento,
                monto_total=monto_total,
                fecha_vencimiento=fecha_vencimiento,
                generado_automaticamente=True,
                justificacion_manual=f"Asistencia Comedor: {self.tipo_comida} - {self.fecha_asistencia}"
            )
            self.adeudo = nuevo_adeudo
            # Guardamos otra vez para registrar el FK del adeudo
            super().save(update_fields=['adeudo'])

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


