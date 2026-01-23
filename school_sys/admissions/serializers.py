from rest_framework import serializers
from .models import VerificationCode, AdmissionUser, Aspirante, AdmissionTutor, AdmissionTutorAspirante
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import random
import re
import json

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
        # El usuario pidió 1 minuto de expiración
        expires_at = timezone.now() + timedelta(minutes=1)
        
        # Eliminar códigos previos no verificados
        VerificationCode.objects.filter(email=email, is_verified=False).delete()
        
        return VerificationCode.objects.create(
            email=email,
            code=code,
            expires_at=expires_at,
            data_json=validated_data.get('data_json')
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

class AspiranteRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    nombre = serializers.CharField(max_length=100)
    apellido_paterno = serializers.CharField(max_length=100)
    apellido_materno = serializers.CharField(max_length=100)
    curp = serializers.CharField(max_length=18)

    def validate_curp(self, value):
        curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9A-Z]{2}$'
        if not re.match(curp_regex, value.upper()):
            raise serializers.ValidationError("Formato de CURP inválido")
        return value.upper()

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
            'fecha_nacimiento', 'sexo', 'direccion', 'telefono', 
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

class AspirantePhase3Serializer(serializers.ModelSerializer):
    """Serializer para Phase 3: Documentación"""
    class Meta:
        model = Aspirante
        fields = [
            'comprobante_domicilio', 'curp_pdf', 'acta_nacimiento_estudiante',
            'acta_nacimiento_tutor', 'curp_tutor_pdf',
            'aceptacion_reglamento', 'autorizacion_imagen'
        ]

    def validate(self, data):
        # Valida que los checks obligatorios vengan en True si se intenta finalizar
        if self.instance.fase_actual == 3:
            if not data.get('aceptacion_reglamento', self.instance.aceptacion_reglamento):
                raise serializers.ValidationError("Debe aceptar el reglamento")
            if not data.get('autorizacion_imagen', self.instance.autorizacion_imagen):
                raise serializers.ValidationError("Debe autorizar el uso de imagen")
        return data
