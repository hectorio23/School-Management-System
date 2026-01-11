"""
Serializers para el endpoint de información del estudiante.
Solo lectura - para consumo del frontend por estudiantes autenticados.
"""
from rest_framework import serializers
from .models import (
    Estudiante, Grado, Grupo, 
    Tutor, EstudianteTutor,
    EstadoEstudiante, HistorialEstadosEstudiante,
    Estrato, EvaluacionSocioeconomica
)
from pagos.models import Adeudo


# =============================================================================
# SERIALIZERS ANIDADOS (Solo lectura)
# =============================================================================

class GradoSerializer(serializers.ModelSerializer):
    """Información del grado académico"""
    class Meta:
        model = Grado
        fields = ["nombre", "nivel"]
        read_only_fields = fields


class GrupoSerializer(serializers.ModelSerializer):
    """Información del grupo con grado anidado"""
    grado = GradoSerializer(read_only=True)
    
    class Meta:
        model = Grupo
        fields = ["nombre", "generacion", "grado"]
        read_only_fields = fields


class TutorEstudianteSerializer(serializers.Serializer):
    """
    Información del tutor asociado al estudiante.
    Incluye el parentesco de la relación.
    """
    tutor_id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(read_only=True)
    apellido_paterno = serializers.CharField(read_only=True)
    apellido_materno = serializers.CharField(read_only=True)
    telefono = serializers.CharField(read_only=True)
    correo = serializers.EmailField(read_only=True)
    parentesco = serializers.CharField(read_only=True)


class TutorUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar información del tutor.
    Valida que ningún campo esté vacío.
    """
    class Meta:
        model = Tutor
        fields = ["id", "nombre", "apellido_paterno", "apellido_materno", "telefono", "correo"]
        read_only_fields = ["id"]
    
    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value.strip()
    
    def validate_apellido_paterno(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El apellido paterno no puede estar vacío.")
        return value.strip()
    
    def validate_apellido_materno(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El apellido materno no puede estar vacío.")
        return value.strip()
    
    def validate_telefono(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El teléfono no puede estar vacío.")
        return value.strip()
    
    def validate_correo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El correo no puede estar vacío.")
        return value.strip()


class EstadoActualSerializer(serializers.ModelSerializer):
    """Estado actual del estudiante (solo el más reciente)"""
    class Meta:
        model = EstadoEstudiante
        fields = ["nombre", "descripcion", "es_estado_activo"]
        read_only_fields = fields


class EvaluacionSocioeconomicaSerializer(serializers.Serializer):
    """
    Evaluación socioeconómica más reciente.
    Campos seleccionados de importancia para el estudiante.
    """
    ingreso_mensual = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tipo_vivienda = serializers.CharField(read_only=True)
    miembros_hogar = serializers.IntegerField(read_only=True)
    estrato_nombre = serializers.CharField(read_only=True)
    porcentaje_descuento = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    aprobado = serializers.BooleanField(read_only=True)
    fecha_evaluacion = serializers.DateTimeField(read_only=True)


class AdeudoResumenSerializer(serializers.ModelSerializer):
    """
    Resumen de adeudos pendientes.
    Solo información esencial, sin detalles de pagos.
    """
    concepto_nombre = serializers.CharField(source="concepto.nombre", read_only=True)
    saldo_pendiente = serializers.SerializerMethodField()
    
    class Meta:
        model = Adeudo
        fields = [
            "concepto_nombre",
            "monto_total", 
            "monto_pagado",
            "saldo_pendiente",
            "estatus",
            "fecha_vencimiento"
        ]
        read_only_fields = fields
    
    def get_saldo_pendiente(self, obj):
        return obj.saldo_pendiente()


# =============================================================================
# SERIALIZER PRINCIPAL
# =============================================================================

class EstudianteInfoSerializer(serializers.ModelSerializer):
    """
    Serializer completo de información del estudiante.
    Incluye todas las relaciones anidadas de solo lectura.
    """
    grupo = GrupoSerializer(read_only=True)
    estado_actual = serializers.SerializerMethodField()
    evaluacion_socioeconomica = serializers.SerializerMethodField()
    tutores = serializers.SerializerMethodField()
    adeudos = serializers.SerializerMethodField()
    balance_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Estudiante
        fields = [
            "matricula",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "direccion",
            "grupo",
            "estado_actual",
            "evaluacion_socioeconomica",
            "tutores",
            "adeudos",
            "balance_total"
        ]
        read_only_fields = fields
    
    def get_estado_actual(self, obj):
        """Obtiene el estado actual del estudiante (el más reciente)"""
        estado = obj.get_estado_actual()
        if estado:
            return EstadoActualSerializer(estado).data
        return None
    
    def get_evaluacion_socioeconomica(self, obj):
        """Obtiene la evaluación socioeconómica más reciente"""
        evaluacion = obj.get_evaluacion_actual()
        if evaluacion:
            return {
                "ingreso_mensual": evaluacion.ingreso_mensual,
                "tipo_vivienda": evaluacion.tipo_vivienda,
                "miembros_hogar": evaluacion.miembros_hogar,
                "estrato_nombre": evaluacion.estrato.nombre if evaluacion.estrato else None,
                "porcentaje_descuento": evaluacion.estrato.porcentaje_descuento if evaluacion.estrato else None,
                "aprobado": evaluacion.aprobado,
                "fecha_evaluacion": evaluacion.fecha_evaluacion
            }
        return None
    
    def get_tutores(self, obj):
        """Obtiene todos los tutores activos del estudiante con su parentesco"""
        relaciones = EstudianteTutor.objects.filter(
            estudiante=obj,
            activo=True
        ).select_related("tutor")
        
        tutores_data = []
        for rel in relaciones:
            tutores_data.append({
                "tutor_id": rel.tutor.id,
                "nombre": rel.tutor.nombre,
                "apellido_paterno": rel.tutor.apellido_paterno,
                "apellido_materno": rel.tutor.apellido_materno,
                "telefono": rel.tutor.telefono,
                "correo": rel.tutor.correo,
                "parentesco": rel.parentesco
            })
        return tutores_data
    
    def get_adeudos(self, obj):
        """Obtiene los adeudos pendientes o parciales (no pagados ni cancelados)"""
        adeudos = Adeudo.objects.filter(
            estudiante=obj,
            estatus__in=["pendiente", "parcial"]
        ).select_related("concepto").order_by("fecha_vencimiento")
        
        return AdeudoResumenSerializer(adeudos, many=True).data
    
    def get_balance_total(self, obj):
        """Calcula el balance total pendiente"""
        return obj.get_balance_total()
