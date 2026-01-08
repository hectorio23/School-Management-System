from django.db import models


#########################################################
# GRADOS Y GRUPOS
#########################################################

class Grade(models.Model):
    name = models.CharField(max_length=50)   # "1°", "2°", "3°"
    level = models.CharField(max_length=100)   # primaria / secundaria / prepa

    def __str__(self):
        return f"{self.name} - {self.level}"


class Group(models.Model):
    name = models.CharField(max_length=100)
    generation = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#########################################################
# ESTUDIANTES
#########################################################

class Student(models.Model):
    enrollment_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    paternal_surname = models.CharField(max_length=255)
    maternal_surname = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.enrollment_number} - {self.name} {self.paternal_surname}"


#########################################################
# TUTORES
#########################################################

class Tutor(models.Model):
    name = models.CharField(max_length=255)
    paternal_surname = models.CharField(max_length=255)
    maternal_surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[+] {self.name} {self.paternal_surname}"


class StudentTutor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=100)
    is_payment_responsible = models.BooleanField(default=False)
    receives_notifications = models.BooleanField(default=True)
    assignment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[+] {self.student} -> {self.tutor} ({self.relationship})"


#########################################################
# ESTADOS DEL ESTUDIANTE
#########################################################

class StudentStatus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class StudentStatusHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.ForeignKey(StudentStatus, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    justification = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[+] {self.student} - {self.status}"


#########################################################
# ESTRATOS SOCIOECONÓMICOS
#########################################################

class Stratum(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SocioeconomicEvaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    housing_type = models.CharField(max_length=255)
    number_of_members = models.IntegerField()
    documents = models.TextField()
    suggested_stratum = models.ForeignKey(Stratum, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[+] - Evaluación {self.student}"


class StratumHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stratum = models.ForeignKey(Stratum, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[+] {self.student} -> {self.stratum}"
