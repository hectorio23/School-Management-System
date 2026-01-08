from django.db import models
from estudiantes.models import Student


class CafeteriaAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=100)
    applied_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.date}"
