
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from estudiantes.models import Estudiante, Tutor, EstudianteTutor
from pagos.models import Pago, Adeudo

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

    class Meta:
        model = Tutor
        fields = ['id', 'nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'correo', 'estudiantes_ids', 'parentesco']

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
                continue # ignorar si no existe el estudiante

        return tutor

# estudiantes
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

class EstudianteAdminSerializer(serializers.ModelSerializer):
    # para crear usuario junto con estudiante
    user_data = UserSerializer(write_only=True)
    
    # ids opcionales
    grado_id = serializers.IntegerField(write_only=True, required=False)
    grupo_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Estudiante
        fields = [
            'matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 
            'direccion', 'user_data', 'grado_id', 'grupo_id'
        ]
        extra_kwargs = {
            'matricula': {'read_only': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user_data')
        grupo_id = validated_data.pop('grupo_id', None)
        # grado_id no se usa directo, queda pendiente

        with transaction.atomic():
            # crear usuario
            user_data['role'] = 'estudiante' # Force role
            user = User.objects.create_user(**user_data)

            # crear estudiante
            estudiante = Estudiante.objects.create(usuario=user, **validated_data)

            # asignar grupo si viene
            if grupo_id:
                # validar que existe? ya veremos
                estudiante.grupo_id = grupo_id
                estudiante.save()
            
            return estudiante

class EstudianteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'direccion', 'grupo']

# pagos
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['fecha_pago']

class AdeudoSerializer(serializers.ModelSerializer):
    pagos = PagoSerializer(many=True, read_only=True, source='pago_set')
    class Meta:
        model = Adeudo
        fields = '__all__'
