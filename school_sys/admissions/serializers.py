import random
import re
import json
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import VerificationCode, AdmissionUser, Aspirante, AdmissionTutor, AdmissionTutorAspirante

# --- SERIALIZADORES DE AUTENTICACIÓN ---

class VerificationCodeSerializer(serializers.ModelSerializer):
    """Maneja la generación y validación de códigos MFA."""
    class Meta:
        model = VerificationCode
        fields = ['email', 'code']
        extra_kwargs = {'code': {'read_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        # Generamos un código de 6 dígitos aleatorios
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Limpieza de códigos antiguos no verificados
        VerificationCode.objects.filter(email=email, is_verified=False).delete()
        
        return VerificationCode.objects.create(
            email=email,
            code=code,
            expires_at=expires_at,
            data_json=validated_data.get('data_json')
        )

class VerifyCodeSerializer(serializers.Serializer):
    """Estructura simple para validar el código recibido."""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

def validate_curp_logic(value):
    """Lógica compartida de validación de formato CURP."""
    curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9A-Z]{2}$'
    if not re.match(curp_regex, value.upper()):
        raise serializers.ValidationError("Formato de CURP inválido")
    return value.upper()

class AspiranteRegistrationSerializer(serializers.Serializer):
    """Paso 1: Captura de credenciales básicas."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class AspiranteConfirmationSerializer(serializers.Serializer):
    """Paso 2: Confirmación de registro con datos personales."""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    nombre = serializers.CharField(max_length=100)
    apellido_paterno = serializers.CharField(max_length=100)
    apellido_materno = serializers.CharField(max_length=100)
    curp = serializers.CharField(max_length=18)

    def validate_curp(self, value):
        return validate_curp_logic(value)

class AspiranteLoginSerializer(serializers.Serializer):
    """Maneja el inicio de sesión y la emisión de tokens JWT."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = AdmissionUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError("Usuario inactivo")
                
                # Generación manual de tokens para asegurar mapeo con 'folio'
                refresh = RefreshToken()
                refresh['user_id'] = user.folio
                
                return {
                    'email': user.email,
                    'folio': user.folio,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            raise serializers.ValidationError("Credenciales inválidas")
        raise serializers.ValidationError("Debe ingresar email y contraseña")

# --- SERIALIZADORES DE FASES (PROCESO) ---

class AdmissionTutorSerializer(serializers.ModelSerializer):
    """Serializa la información de los tutores asociados."""
    parentesco = serializers.CharField(write_only=True, required=False, default="Tutor")
    
    class Meta:
        model = AdmissionTutor
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'email', 'numero_telefono', 'curp', 'parentesco']

class AspirantePhase1Serializer(serializers.ModelSerializer):
    """Fase 1: Datos personales extendidos y tutores."""
    tutores = AdmissionTutorSerializer(many=True, required=False)
    
    class Meta:
        model = Aspirante
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno', 'curp', 
            'fecha_nacimiento', 'sexo', 'direccion', 'telefono', 
            'escuela_procedencia', 'promedio_anterior', 'tutores'
        ]

    def validate_curp(self, value):
        return validate_curp_logic(value) if value else value

    def update(self, instance, validated_data):
        tutores_data = validated_data.pop('tutores', [])
        with transaction.atomic():
            # Actualización de datos base
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Avance automático de fase
            if instance.fase_actual == 1:
                instance.fase_actual = 2
            
            instance.save()
            
            # Sincronización de tutores
            if tutores_data:
                for t_data in tutores_data:
                    parentesco = t_data.pop('parentesco', 'Tutor')
                    tutor, _ = AdmissionTutor.objects.get_or_create(
                        email=t_data.get('email'),
                        defaults=t_data
                    )
                    AdmissionTutorAspirante.objects.update_or_create(
                        aspirante=instance,
                        tutor=tutor,
                        defaults={'parentesco': parentesco}
                    )
        return instance

class AspirantePhase3Serializer(serializers.ModelSerializer):
    """Fase 3: Carga de documentos y validación legal."""
    class Meta:
        model = Aspirante
        fields = [
            'curp_pdf', 'acta_nacimiento', 'foto_credencial',
            'boleta_ciclo_anterior', 'boleta_ciclo_actual',
            'aceptacion_reglamento', 'autorizacion_imagen',
            # Campos virtuales (se procesan en la vista pero el serializer los permite)
            'acta_nacimiento_tutor', 'comprobante_domicilio_tutor', 
            'foto_fachada_domicilio', 'comprobante_ingresos', 
            'carta_ingresos', 'ine_tutor', 'contrato_arrendamiento_predial',
            'carta_bajo_protesta'
        ]

    # Declaramos los campos del tutor como FileFields opcionales no ligados al modelo Aspirante
    acta_nacimiento_tutor = serializers.FileField(required=False)
    comprobante_domicilio_tutor = serializers.FileField(required=False)
    foto_fachada_domicilio = serializers.FileField(required=False)
    comprobante_ingresos = serializers.FileField(required=False)
    carta_ingresos = serializers.FileField(required=False)
    ine_tutor = serializers.FileField(required=False)
    contrato_arrendamiento_predial = serializers.FileField(required=False)
    carta_bajo_protesta = serializers.FileField(required=False)

    def validate(self, data):
        """Valida que los acuerdos legales estén aceptados al finalizar fase."""
        if self.instance.fase_actual == 3:
            if not data.get('aceptacion_reglamento', self.instance.aceptacion_reglamento):
                raise serializers.ValidationError("Debe aceptar el reglamento")
            if not data.get('autorizacion_imagen', self.instance.autorizacion_imagen):
                raise serializers.ValidationError("Debe autorizar el uso de imagen")
        return data
