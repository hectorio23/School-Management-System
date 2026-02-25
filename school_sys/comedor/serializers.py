from rest_framework import serializers
from .models import Menu, AsistenciaCafeteria, MenuSemanal
from estudiantes.models import Estudiante

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuSemanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSemanal
        fields = '__all__'

class AsistenciaCafeteriaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    estudiante_matricula = serializers.SerializerMethodField()
    
    class Meta:
        model = AsistenciaCafeteria
        fields = [
            'id', 'estudiante', 'estudiante_nombre', 'estudiante_matricula', 'menu', 
            'fecha_asistencia', 'tipo_comida', 'precio_aplicado', 'fecha_registro'
        ]
        read_only_fields = ['fecha_registro', 'precio_aplicado']

    def get_estudiante_nombre(self, obj):
        return f"{obj.estudiante.nombre} {obj.estudiante.apellido_paterno} {obj.estudiante.apellido_materno}"
        
    def get_estudiante_matricula(self, obj):
        return obj.estudiante.matricula

class EstudianteAlergiaSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    grado_grupo = serializers.SerializerMethodField()

    class Meta:
        model = Estudiante
        fields = ['matricula', 'nombre_completo', 'alergias_alimentarias', 'grado_grupo']

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    
    def get_grado_grupo(self, obj):
        grupo = obj.grupo_actual
        if grupo:
            return f"{grupo.grado.nombre} {grupo.nombre}"
        return "Sin grupo"
