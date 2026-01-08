from rest_framework import serializers
from .models import Student

class SerializerStudents(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["enrollment_number", "name", "paternal_surname", "maternal_surname", "username", "created_at", "address", "group"]
