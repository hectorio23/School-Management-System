from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Student, StudentStatusHistory, StratumHistory


@receiver(pre_save, sender=Student)
def generate_histories(sender, instance, **kwargs):
    if not instance.pk:
        return  # only run on updates

    try:
        previous = Student.objects.get(pk=instance.pk)
    except Student.DoesNotExist:
        return

    # STATUS HISTORY
    if previous.current_status != instance.current_status and instance.current_status:
        StudentStatusHistory.objects.create(
            student=instance,
            status=instance.current_status
        )

    # STRATUM HISTORY
    if previous.current_stratum != instance.current_stratum and instance.current_stratum:
        StratumHistory.objects.create(
            student=instance,
            stratum=instance.current_stratum
        )
