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

# --- VALIDACIÓN DE DOCUMENTOS ---

ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
ALLOWED_MIME_TYPES = [
    'application/pdf',
    'image/jpeg',
    'image/png',
]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_document_file(file_obj):
    """
    Valida que un archivo sea PDF o imagen (JPG, PNG).
    Verifica extensión, tipo MIME y tamaño máximo.
    """
    if not file_obj:
        return file_obj
    
    # Verificar tamaño
    if hasattr(file_obj, 'size') and file_obj.size > MAX_FILE_SIZE:
        raise serializers.ValidationError(
            f"El archivo excede el tamaño máximo permitido de 10MB. Tamaño actual: {file_obj.size / (1024*1024):.2f}MB"
        )
    
    # Verificar extensión
    file_name = file_obj.name.lower() if hasattr(file_obj, 'name') else ''
    extension = file_name.split('.')[-1] if '.' in file_name else ''
    if extension not in ALLOWED_EXTENSIONS:
        raise serializers.ValidationError(
            f"Extensión no permitida: .{extension}. Solo se aceptan: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Verificar tipo MIME (content_type)
    content_type = getattr(file_obj, 'content_type', None)
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        raise serializers.ValidationError(
            f"Tipo de archivo no permitido: {content_type}. Solo se aceptan PDF e imágenes (JPG, PNG)"
        )
    
    return file_obj

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
        fields = [
            'id', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 
            'numero_telefono', 'curp', 'parentesco',
            'acta_nacimiento', 'curp_pdf', 'comprobante_domicilio', 
            'comprobante_ingresos', 'carta_ingresos', 
            'ine_tutor', 'contrato_arrendamiento_predial', 'carta_bajo_protesta'
        ]
        read_only_fields = ['id']

class AdmissionTutorPhase1Serializer(serializers.ModelSerializer):
    """Versión simplificada para Fase 1 (evita validación de archivos en JSON)."""
    parentesco = serializers.CharField(required=False, default="Tutor")
    
    class Meta:
        model = AdmissionTutor
        fields = [
            'id', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 
            'numero_telefono', 'curp', 'parentesco'
        ]
        read_only_fields = ['id']

class AdmissionTutorDetailSerializer(serializers.ModelSerializer):
    """Información completa del tutor para vista administrativa."""
    class Meta:
        model = AdmissionTutor
        fields = '__all__'

class AspiranteDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el expediente completo del aspirante."""
    folio = serializers.IntegerField(source='user.folio', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    tutores = serializers.SerializerMethodField()
    documentos = serializers.SerializerMethodField()
    
    class Meta:
        model = Aspirante
        fields = '__all__'

    def get_tutores(self, obj):
        rels = AdmissionTutorAspirante.objects.filter(aspirante=obj)
        data = []
        for rel in rels:
            tutor_data = AdmissionTutorDetailSerializer(rel.tutor).data
            tutor_data['parentesco'] = rel.parentesco
            data.append(tutor_data)
        return data

    def get_documentos(self, obj):
        # Generar lista de URLs de documentos dinámicamente
        docs = []
        folio = obj.user.folio
        
        # Docs Aspirante
        student_fields = [
            ('curp_pdf', 'CURP Aspirante'),
            ('acta_nacimiento', 'Acta de Nacimiento Aspirante'),
            ('foto_credencial', 'Foto Credencial'),
            ('boleta_ciclo_anterior', 'Boleta Ciclo Anterior'),
            ('boleta_ciclo_actual', 'Boleta Ciclo Actual'),
            ('foto_fachada_domicilio', 'Foto Fachada Domicilio')
        ]
        
        for field, label in student_fields:
            if getattr(obj, field, None):
                docs.append({
                    "entity": "aspirante",
                    "field": field,
                    "label": label,
                    "url": f"/api/admission/admin/aspirante/{folio}/document/{field}/"
                })
        
        # Docs Tutores
        rels = AdmissionTutorAspirante.objects.filter(aspirante=obj)
        tutor_fields = [
            ('acta_nacimiento', 'Acta de Nacimiento'),
            ('curp_pdf', 'CURP'),
            ('comprobante_domicilio', 'Comprobante Domicilio'),
            ('comprobante_ingresos', 'Comprobante Ingresos'),
            ('carta_ingresos', 'Carta Ingresos'),
            ('ine_tutor', 'INE'),
            ('contrato_arrendamiento_predial', 'Contrato/Predial'),
            ('carta_bajo_protesta', 'Carta Bajo Protesta')
        ]
        
        for rel in rels:
            tutor = rel.tutor
            for field, label in tutor_fields:
                if getattr(tutor, field, None):
                    docs.append({
                        "entity": f"tutor_{tutor.id}",
                        "tutor_id": tutor.id,
                        "tutor_nombre": tutor.nombre,
                        "field": field,
                        "label": f"{label} ({tutor.nombre})",
                        "url": f"/api/admission/admin/tutor/{tutor.id}/document/{field}/"
                    })
        return docs

class AspirantePhase1Serializer(serializers.ModelSerializer):
    """Fase 1: Datos personales extendidos y tutores."""
    tutores = AdmissionTutorPhase1Serializer(many=True, required=False)
    
    class Meta:
        model = Aspirante
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno', 'curp', 
            'fecha_nacimiento', 'sexo', 'direccion', 'telefono', 
            'escuela_procedencia', 'promedio_anterior', 'nivel_ingreso', 
            'foto_fachada_domicilio', 'tutores'
        ]

    def to_internal_value(self, data):
        # Support stringified JSON for 'tutores' when using multipart/form-data
        if 'tutores' in data and isinstance(data.get('tutores'), str):
            import json
            try:
                # Need to convert QueryDict to a mutable dict to update it
                mutable_data = data.dict() if hasattr(data, 'dict') else data.copy()
                mutable_data['tutores'] = json.loads(data.get('tutores'))
                return super().to_internal_value(mutable_data)
            except (ValueError, TypeError) as e:
                pass
        return super().to_internal_value(data)

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
                # Obtenemos archivos del request si están disponibles (vía context)
                request = self.context.get('request')
                files = request.FILES if request else {}

                for i, t_data in enumerate(tutores_data):
                    parentesco = t_data.pop('parentesco', 'Tutor')
                    email = t_data.get('email')
                    
                    if not email: continue

                    tutor, created = AdmissionTutor.objects.get_or_create(
                        email=email,
                        defaults=t_data
                    )
                    
                    # Si no fue creado, actualizamos datos básicos
                    if not created:
                        for attr, value in t_data.items():
                            setattr(tutor, attr, value)
                    
                    # Manejo de archivos específicos para este tutor: tutor_0_ine_tutor, tutor_1_ine_tutor...
                    tutor_file_fields = [
                        'acta_nacimiento', 'curp_pdf', 'comprobante_domicilio', 
                        'comprobante_ingresos', 'carta_ingresos', 
                        'ine_tutor', 'contrato_arrendamiento_predial', 'carta_bajo_protesta'
                    ]
                    for field in tutor_file_fields:
                        specific_key = f'tutor_{i}_{field}'
                        if specific_key in files:
                            setattr(tutor, field, files[specific_key])
                        elif field in files and len(tutores_data) == 1:
                            # Si solo hay uno, permitimos nombres de campo genéricos
                            setattr(tutor, field, files[field])

                    tutor.save()
                    
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
            'foto_fachada_domicilio', 'boleta_ciclo_anterior', 'boleta_ciclo_actual',
            'aceptacion_reglamento', 'autorizacion_imagen',
        ]
        extra_kwargs = {
            'curp_pdf': {'required': True},
            'acta_nacimiento': {'required': True},
            'foto_credencial': {'required': True},
            'boleta_ciclo_anterior': {'required': True},
            'boleta_ciclo_actual': {'required': False},
        }



    def validate(self, data):
        """Valida que los acuerdos legales estén aceptados al finalizar fase."""
        if self.instance.fase_actual == 3:
            if not data.get('aceptacion_reglamento', self.instance.aceptacion_reglamento):
                raise serializers.ValidationError("Debe aceptar el reglamento")
            if not data.get('autorizacion_imagen', self.instance.autorizacion_imagen):
                raise serializers.ValidationError("Debe autorizar el uso de imagen")
            
            # Validación condicional de boleta actual
            nivel = self.instance.nivel_ingreso
            # Para secundaria y preparatoria ES requerida
            if nivel not in ['PREESCOLAR', 'PRIMARIA']:
                current_file = self.instance.boleta_ciclo_actual
                new_file = data.get('boleta_ciclo_actual')
                if not current_file and not new_file:
                     raise serializers.ValidationError({"boleta_ciclo_actual": "Este documento es requerido para el nivel seleccionado."})

        return data

    # --- Validadores de documentos del aspirante ---
    def validate_curp_pdf(self, value):
        return validate_document_file(value)
    
    def validate_acta_nacimiento(self, value):
        return validate_document_file(value)
    
    def validate_foto_credencial(self, value):
        return validate_document_file(value)
    
    def validate_boleta_ciclo_anterior(self, value):
        return validate_document_file(value)
    
    def validate_boleta_ciclo_actual(self, value):
        return validate_document_file(value)

    # --- Validadores de documentos del tutor ---
    def validate_acta_nacimiento_tutor(self, value):
        return validate_document_file(value)
    
    def validate_comprobante_domicilio_tutor(self, value):
        return validate_document_file(value)
    
    def validate_foto_fachada_domicilio(self, value):
        return validate_document_file(value)
    
    def validate_comprobante_ingresos(self, value):
        return validate_document_file(value)
    
    def validate_carta_ingresos(self, value):
        return validate_document_file(value)
    
    def validate_ine_tutor(self, value):
        return validate_document_file(value)
    
    def validate_contrato_arrendamiento_predial(self, value):
        return validate_document_file(value)
    
    def validate_carta_bajo_protesta(self, value):
        return validate_document_file(value)
    
    def validate_curp_pdf_tutor(self, value):
        return validate_document_file(value)

class AspiranteAdminListSerializer(serializers.ModelSerializer):
    """Serializer para listado administrativo de aspirantes."""
    folio = serializers.IntegerField(source='user.folio', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Aspirante
        fields = [
            'folio', 'nombre', 'apellido_paterno', 'apellido_materno', 
            'email', 'status', 'fase_actual', 'nivel_ingreso', 'curp',
            'telefono', 'fecha_pago', 'monto', 'metodo_pago',
            'pagado_status'
        ]

