from rest_framework import serializers
from .models import VerificationCode, AdmissionUser, Aspirante, AdmissionTutor, AdmissionTutorAspirante
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import random
import re

class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['email', 'code']
        extra_kwargs = {
            'code': {'read_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        # Generar código de 6 dígitos
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Eliminar códigos previos no verificados
        VerificationCode.objects.filter(email=email, is_verified=False).delete()
        
        return VerificationCode.objects.create(
            email=email,
            code=code,
            expires_at=expires_at
        )

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class AdmissionUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = AdmissionUser
        fields = ['folio', 'email', 'password']
        read_only_fields = ['folio']

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        # Usamos make_password para ser consistentes con seguridad estándar
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class RegisterAspiranteSerializer(serializers.ModelSerializer):
    user_data = AdmissionUserSerializer(source='user')
    
    class Meta:
        model = Aspirante
        fields = ['user_data', 'nombre', 'apellido_paterno', 'apellido_materno']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        # Crear usuario
        user = AdmissionUser.objects.create(
            email=user_data['email'],
            password=user_data['password'],
            is_verified=True # Ya verificado previamente
        )
        # Crear aspirante vacio inicial
        aspirante = Aspirante.objects.create(user=user, **validated_data)
        return aspirante

# --- PHASE SERIALIZERS ---

class AdmissionTutorSerializer(serializers.ModelSerializer):
    parentesco = serializers.CharField(write_only=True, required=False, default="Tutor")
    
    class Meta:
        model = AdmissionTutor
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'email', 'numero_telefono', 'curp', 'parentesco']

class AspirantePhase1Serializer(serializers.ModelSerializer):
    tutores = AdmissionTutorSerializer(many=True, required=False)
    
    class Meta:
        model = Aspirante
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno', 'curp', 
            'fecha_nacimiento', 'genero', 'direccion', 'telefono', 
            'escuela_procedencia', 'promedio_anterior', 'tutores'
        ]

    def validate_curp(self, value):
        if value:
            # Regex básica de CURP mexicano (18 caracteres)
            curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9A-Z]{2}$'
            if not re.match(curp_regex, value.upper()):
                raise serializers.ValidationError("Formato de CURP inválido")
        return value.upper()

    def update(self, instance, validated_data):
        tutores_data = validated_data.pop('tutores', [])
        
        with transaction.atomic():
            # Actualizar datos del aspirante
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Avanzar fase si es necesario
            if instance.fase_actual == 1:
                instance.fase_actual = 2
            
            instance.save()
            
            # Manejar tutores
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
