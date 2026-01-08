from django.db import models
from estudiantes.models import Student


class PaymentConcept(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    educational_level = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Debt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    concept = models.ForeignKey(PaymentConcept, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    generation_date = models.DateField()
    due_date = models.DateField()
    applied_surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"[+] - Adeudos {self.student} -> {self.concept}"


class Payment(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100)
    receipt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[+] - Pago {self.amount} - {self.date}"
