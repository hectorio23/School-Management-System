
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from estudiantes.models import Estudiante, Tutor, EstudianteTutor, Grupo, Grado, EvaluacionSocioeconomica
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
    parentesco = serializers.CharField(
        required=False, 
        write_only=True, 
        default="Tutor",
        help_text="Parentesco para la vinculación (solo al crear)"
    )
    
    # Campos de solo lectura
    estudiantes = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = ['id', 'nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'correo', 'estudiantes_ids', 'parentesco', 'estudiantes']

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

    def create(self, validated_data):
        estudiantes_ids = validated_data.pop('estudiantes_ids', [])
        parentesco = validated_data.pop('parentesco', 'Tutor')
        
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
