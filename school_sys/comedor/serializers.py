from rest_framework import serializers
from .models import Menu, AsistenciaCafeteria, AdeudoComedor, MenuSemanal
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
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    
    class Meta:
        model = AsistenciaCafeteria
        fields = [
            'id', 'estudiante', 'estudiante_nombre', 'menu', 
            'fecha_asistencia', 'tipo_comida', 'precio_aplicado', 'fecha_registro'
        ]
        read_only_fields = ['fecha_registro', 'precio_aplicado']

class AdeudoComedorSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre_completo', read_only=True)
    
    class Meta:
        model = AdeudoComedor
        fields = [
            'id', 'estudiante', 'estudiante_nombre', 'asistencia', 'adeudo',
            'monto', 'fecha_generacion', 'fecha_vencimiento', 
            'recargo_aplicado', 'monto_total', 'pagado'
        ]
        read_only_fields = ['pagado']

class EstudianteAlergiaSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    grado_grupo = serializers.SerializerMethodField()

    class Meta:
        model = Estudiante
        fields = ['matricula', 'nombre_completo', 'alergias_alimentarias', 'grado_grupo']

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    
    def get_grado_grupo(self, obj):
        if obj.grupo:
            return f"{obj.grupo.grado.nombre} {obj.grupo.nombre}"
        return "Sin grupo"
