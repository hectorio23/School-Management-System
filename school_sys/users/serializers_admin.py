
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from estudiantes.models import (
    Estudiante, Tutor, EstudianteTutor, Grupo, Grado, 
    EvaluacionSocioeconomica, Estrato, EstadoEstudiante,
    Beca, BecaEstudiante
)
from pagos.models import Pago, Adeudo, ConceptoPago
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# tutores
class TutorSerializer(serializers.ModelSerializer):
    estudiantes_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        required=False, 
        write_only=True,
        help_text="Lista de matrículas de estudiantes a vincular"
    )
    parentesco = serializers.SerializerMethodField()
    
    # Campo para escritura (solo al crear/actualizar)
    parentesco_input = serializers.CharField(
        write_only=True, 
        required=False,
        default="Tutor",
        help_text="Parentesco para la vinculación (solo al crear/actualizar)"
    )
    
    # Campos de solo lectura
    estudiantes = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = ['id', 'nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'correo', 'estudiantes_ids', 'parentesco', 'parentesco_input', 'estudiantes']

    def get_estudiantes(self, obj):
        # Retorna una simple tupla -> (matricula, nombre)
        data = []
        rels = obj.estudiantetutor_set.select_related('estudiante').all()
        for r in rels:
            e = r.estudiante
            data.append({
                "matricula": e.matricula,
                "nombre_completo": f"{e.nombre} {e.apellido_paterno} {e.apellido_materno}",
                "parentesco": r.parentesco
            })
        return data

    def get_parentesco(self, obj):
        # Retorna el primer parentesco encontrado en sus relaciones
        rel = obj.estudiantetutor_set.first()
        return rel.parentesco if rel else ""

    def create(self, validated_data):
        estudiantes_ids = validated_data.pop('estudiantes_ids', [])
        parentesco = validated_data.pop('parentesco_input', 'Tutor')
        
        tutor = Tutor.objects.create(**validated_data)
        
        # vincular estudiantes en caso de que se especifiquen
        for matricula in estudiantes_ids:
            try:
                estudiante = Estudiante.objects.get(matricula=matricula)
                EstudianteTutor.objects.create(
                    estudiante=estudiante,
                    tutor=tutor,
                    parentesco=parentesco
                )
            except Estudiante.DoesNotExist:
                continue 

        return tutor

# estudiantes
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

class EstudianteAdminSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(write_only=True)
    grado_id = serializers.IntegerField(write_only=True, required=False)
    grupo_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Estudiante
        fields = [
            'matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 
            'direccion', 'porcentaje_beca', 'user_data', 'grado_id', 'grupo_id'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user_data')
        grupo_id = validated_data.pop('grupo_id', None)

        with transaction.atomic():
            user_data['role'] = 'estudiante'
            user = User.objects.create_user(**user_data)

            estudiante = Estudiante.objects.create(usuario=user, **validated_data)

            if grupo_id:
                estudiante.grupo_id = grupo_id
                estudiante.save()
            
            return estudiante

class EstudianteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'direccion', 'grupo', 'porcentaje_beca']

# estratos
class AdeudoCreateSerializer(serializers.Serializer):
    estudiante_matricula = serializers.IntegerField()
    concepto_id = serializers.IntegerField()
    
    def create(self, validated_data):
        print("Creating Adeudo with logic...")
        matricula = validated_data['estudiante_matricula']
        concepto_id = validated_data['concepto_id']
        
        estudiante = Estudiante.objects.get(matricula=matricula)
        concepto = ConceptoPago.objects.get(id=concepto_id)
        
        # Cacular el descuento
        estrato = estudiante.get_estrato_actual()
        porcentaje_estrato = estrato.porcentaje_descuento if estrato else 0
        porcentaje_beca = estudiante.porcentaje_beca # Decimal
        
        total_descuento_pct = porcentaje_estrato + porcentaje_beca
        if total_descuento_pct > 100:
            total_descuento_pct = 100
        
        monto_base = concepto.monto_base
        descuento_monto = (monto_base * total_descuento_pct) / 100
        monto_total = monto_base - descuento_monto
        
        # Comprobar que el campo sea de tipo date y no datetime (da error si es datetime)
        fecha_vencimiento = (timezone.now() + timedelta(days=30)).date()

        adeudo = Adeudo.objects.create(
            estudiante=estudiante,
            concepto=concepto,
            monto_base=monto_base,
            descuento_aplicado=descuento_monto,
            monto_total=monto_total,
            estatus='pendiente',
            fecha_vencimiento=fecha_vencimiento
        )
        return adeudo

class AdeudoSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre', read_only=True)
    estudiante_apellido = serializers.CharField(source='estudiante.apellido_paterno', read_only=True)
    concepto_nombre = serializers.CharField(source='concepto.nombre', read_only=True)

    class Meta:
        model = Adeudo
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    estudiante_matricula = serializers.IntegerField(source='adeudo.estudiante.matricula', read_only=True)
    estudiante_nombre = serializers.CharField(source='adeudo.estudiante.nombre', read_only=True)
    estudiante_apellido = serializers.CharField(source='adeudo.estudiante.apellido_paterno', read_only=True)
    concepto = serializers.CharField(source='adeudo.concepto.nombre', read_only=True)

    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['fecha_pago']

class EvaluacionSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre', read_only=True)
    estudiante_apellido = serializers.CharField(source='estudiante.apellido_paterno', read_only=True)
    estrato_nombre = serializers.CharField(source='estrato.nombre', read_only=True)

    class Meta:
        model = EvaluacionSocioeconomica
        fields = '__all__'


# =============================================================================
# SERIALIZERS PARA CATALOGOS (CRUD)
# =============================================================================

class ConceptoPagoSerializer(serializers.ModelSerializer):
    """Serializer para ConceptoPago con campos para generación masiva"""
    # Campos para generación masiva (write_only)
    aplicar_a_nivel = serializers.CharField(required=False, write_only=True, allow_blank=True)
    aplicar_a_grado = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    aplicar_a_grupo = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    aplicar_a_estrato = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    aplicar_a_matricula = serializers.CharField(required=False, write_only=True, allow_blank=True)

    class Meta:
        model = ConceptoPago
        fields = [
            'id', 'nombre', 'descripcion', 'monto_base', 'activo', 'nivel_educativo',
            'aplicar_a_nivel', 'aplicar_a_grado', 'aplicar_a_grupo', 
            'aplicar_a_estrato', 'aplicar_a_matricula'
        ]


class GradoSerializer(serializers.ModelSerializer):
    """Serializer para Grado"""
    class Meta:
        model = Grado
        fields = ['id', 'nombre', 'nivel']


class GrupoSerializer(serializers.ModelSerializer):
    """Serializer para Grupo con grado anidado"""
    grado_nombre = serializers.CharField(source='grado.nombre', read_only=True)
    grado_nivel = serializers.CharField(source='grado.nivel', read_only=True)
    
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'generacion', 'descripcion', 'grado', 'grado_nombre', 'grado_nivel']


class EstratoSerializer(serializers.ModelSerializer):
    """Serializer para Estrato socioeconómico"""
    class Meta:
        model = Estrato
        fields = [
            'id', 'nombre', 'descripcion', 'porcentaje_descuento', 
            'activo', 'color', 'ingreso_minimo', 'ingreso_maximo'
        ]


class EstadoEstudianteSerializer(serializers.ModelSerializer):
    """Serializer para EstadoEstudiante"""
    class Meta:
        model = EstadoEstudiante
        fields = ['id', 'nombre', 'descripcion', 'es_estado_activo']


class BecaSerializer(serializers.ModelSerializer):
    """Serializer para Beca"""
    estudiantes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Beca
        fields = [
            'id', 'nombre', 'descripcion', 'porcentaje', 
            'fecha_inicio', 'fecha_vencimiento', 'valida', 'estudiantes_count'
        ]
    
    def get_estudiantes_count(self, obj):
        return obj.becaestudiante_set.filter(activa=True).count()


class BecaEstudianteSerializer(serializers.ModelSerializer):
    """Serializer para asignación de becas a estudiantes"""
    estudiante_matricula = serializers.IntegerField(source='estudiante.matricula', read_only=True)
    estudiante_nombre = serializers.CharField(source='estudiante.nombre', read_only=True)
    estudiante_apellido = serializers.CharField(source='estudiante.apellido_paterno', read_only=True)
    beca_nombre = serializers.CharField(source='beca.nombre', read_only=True)
    beca_porcentaje = serializers.DecimalField(source='beca.porcentaje', max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = BecaEstudiante
        fields = [
            'id', 'beca', 'estudiante', 'activa', 
            'fecha_asignacion', 'fecha_retiro', 'motivo_retiro', 'asignado_por',
            'estudiante_matricula', 'estudiante_nombre', 'estudiante_apellido',
            'beca_nombre', 'beca_porcentaje'
        ]
        read_only_fields = ['fecha_asignacion']
