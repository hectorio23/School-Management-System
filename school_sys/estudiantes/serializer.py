from rest_framework import serializers
from .models import Estudiante

class SerializerStudent(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ["matricula", "nombre", "apellido_paterno", "apellido_materno", "nombre_usuario", "fecha_creacion", "direccion"]
