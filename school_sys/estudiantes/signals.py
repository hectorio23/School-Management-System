from django.db.models.signals import post_save
from django.dispatch import receiver
from pagos.models import Adeudo, Pago
from .services import procesar_reinscripcion_automatica

@receiver(post_save, sender=Pago)
def trigger_reinscripcion_on_pago(sender, instance, created, **kwargs):
    """
    Cuando se registra un Pago, verificamos si liquidó un adeudo de reinscripción.
    """
    if instance.adeudo and instance.adeudo.estatus == 'pagado':
        if instance.adeudo.concepto.tipo_concepto == 'reinscripcion':
            procesar_reinscripcion_automatica(instance)

@receiver(post_save, sender=Adeudo)
def trigger_reinscripcion_on_adeudo(sender, instance, created, **kwargs):
    """
    En caso de que el adeudo se marque como pagado manualmente o por otra vía.
    """
    if instance.estatus == 'pagado' and instance.concepto.tipo_concepto == 'reinscripcion':
        procesar_reinscripcion_automatica(instance)
