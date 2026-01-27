import json
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsAdministrador
from .permissions import IsAspirante
from .authentication import AdmissionJWTAuthentication
from .utils_security import decrypt_data
from .models import VerificationCode, AdmissionUser, Aspirante, AdmissionTutorAspirante
from .serializers import (
    VerificationCodeSerializer, 
    VerifyCodeSerializer, 
    AspiranteRegistrationSerializer,
    AspiranteConfirmationSerializer,
    AspirantePhase1Serializer,
    AspirantePhase3Serializer,
    AspiranteLoginSerializer
)

# --- ENDPOINTS DE AUTENTICACIÓN ---

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Acceso para aspirantes. Retorna tokens JWT."""
    serializer = AspiranteLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_initiate(request):
    """Paso 1: Recibe email/contraseña y genera código de verificación."""
    serializer = AspiranteRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        if AdmissionUser.objects.filter(email=email).exists():
            return Response({"error": "El correo ya está registrado"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Almacenamos credenciales temporales en JSON
        data_json = json.dumps(serializer.validated_data)
        v_serializer = VerificationCodeSerializer(data={"email": email})
        if v_serializer.is_valid():
            verification = v_serializer.save(data_json=data_json)
            return Response({
                "message": f"Código enviado a { email }",
                "expired_at": timezone.now() + timedelta(minutes=10), 
                "code_debug": verification.code
            }, status=status.HTTP_201_CREATED)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_confirm(request):
    """Paso 2: Verifica código y recibe datos personales para crear la cuenta definitiva."""
    serializer = AspiranteConfirmationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    code = serializer.validated_data['code']
        
    try:
        verification = VerificationCode.objects.get(email=email, code=code, is_verified=False)
        if not verification.is_valid():
             return Response({"error": "Código expirado o inválido"}, status=status.HTTP_400_BAD_REQUEST)
             
        # Cargar credenciales del Paso 1
        credentials = json.loads(verification.data_json)
        from django.contrib.auth.hashers import make_password
        
        with transaction.atomic():
            user = AdmissionUser.objects.create(
                email=credentials['email'],
                password=make_password(credentials['password']),
                is_verified=True
            )
            Aspirante.objects.create(
                user=user,
                nombre=serializer.validated_data['nombre'],
                apellido_paterno=serializer.validated_data['apellido_paterno'],
                apellido_materno=serializer.validated_data['apellido_materno'],
                curp=serializer.validated_data['curp']
            )
            verification.is_verified = True
            verification.save()
            
            return Response({
                "message": "Registro completado exitosamente",
                "folio": user.folio,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
            
    except VerificationCode.DoesNotExist:
        return Response({"error": "Código o correo inválido"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- ENDPOINTS DE FASES DE ADMISIÓN ---

@api_view(['GET'])
@authentication_classes([AdmissionJWTAuthentication])
@permission_classes([IsAuthenticated, IsAspirante])
def aspirante_me(request, folio):
    """Obtiene el estado actual y datos del aspirante basado en su folio."""
    if request.user.folio != folio:
        return Response({"error": "No tienes permiso para acceder a esta información"}, status=status.HTTP_403_FORBIDDEN)

    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    serializer = AspirantePhase1Serializer(aspirante)
    data = serializer.data
    data.update({
        'fase_actual': aspirante.fase_actual,
        'status': aspirante.status,
        'pagado_status': aspirante.pagado_status
    })
    return Response(data)

@api_view(['PUT'])
@authentication_classes([AdmissionJWTAuthentication])
@permission_classes([IsAuthenticated, IsAspirante])
def aspirante_phase1(request, folio):
    """Fase 1: Actualización de datos personales y registro de tutores."""
    if request.user.folio != folio:
        return Response({"error": "No tienes permiso para modificar esta información"}, status=status.HTTP_403_FORBIDDEN)

    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    serializer = AspirantePhase1Serializer(aspirante, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Fase 1 OK", "fase_actual": aspirante.fase_actual})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([AdmissionJWTAuthentication])
@permission_classes([IsAuthenticated, IsAspirante])
def aspirante_phase2(request, folio):
    """Fase 2: Registro de información socioeconómica."""
    if request.user.folio != folio:
        return Response({"error": "No tienes permiso para modificar esta información"}, status=status.HTTP_403_FORBIDDEN)

    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    if aspirante.fase_actual < 2:
         return Response({"error": "Complete Fase 1 primero"}, status=status.HTTP_400_BAD_REQUEST)
    
    fields = [
        'ingreso_mensual_familiar', 'ocupacion_padre', 'ocupacion_madre', 
        'tipo_vivienda', 'miembros_hogar', 'vehiculos', 'internet_encasa'
    ]
    for f in fields:
        if f in request.data: setattr(aspirante, f, request.data[f])
    
    if aspirante.fase_actual == 2: aspirante.fase_actual = 3
    aspirante.save()
    return Response({"message": "Fase 2 OK", "fase_actual": aspirante.fase_actual})

@api_view(['PUT'])
@authentication_classes([AdmissionJWTAuthentication])
@permission_classes([IsAuthenticated, IsAspirante])
def aspirante_phase3(request, folio):
    """Fase 3: Carga de documentación digital y aceptación legal."""
    if request.user.folio != folio:
        return Response({"error": "No tienes permiso para modificar esta información"}, status=status.HTTP_403_FORBIDDEN)

    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    if aspirante.fase_actual < 3:
         return Response({"error": "Complete Fase 2 primero"}, status=status.HTTP_400_BAD_REQUEST)
         
    serializer = AspirantePhase3Serializer(aspirante, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                # 1. Documentos del aspirante
                for field in ['comprobante_domicilio', 'curp_pdf', 'acta_nacimiento_estudiante']:
                    if field in request.FILES:
                        setattr(aspirante, field, request.FILES[field])
                
                # 2. Documentos del tutor (asociados al primer registro de relación)
                tutor_rel = AdmissionTutorAspirante.objects.filter(aspirante=aspirante).first()
                if tutor_rel:
                    tutor = tutor_rel.tutor
                    tutor_updated = False
                    if 'acta_nacimiento_tutor' in request.FILES:
                        tutor.acta_nacimiento = request.FILES['acta_nacimiento_tutor']
                        tutor_updated = True
                    if 'curp_tutor_pdf' in request.FILES:
                        tutor.curp_pdf = request.FILES['curp_tutor_pdf']
                        tutor_updated = True
                    if tutor_updated:
                        tutor.save()

                serializer.save()
                
                # Actualización de validaciones internas
                if aspirante.acta_nacimiento_estudiante: aspirante.acta_nacimiento_check = True
                if aspirante.curp_pdf: aspirante.curp_check = True
                
                if aspirante.fase_actual == 3: 
                    aspirante.fase_actual = 4
                
                aspirante.save()
            return Response({"message": "Fase 3 OK. Pendiente de Pago.", "fase_actual": aspirante.fase_actual})
        except Exception as e:
            return Response({"error": f"Error al procesar archivos: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- ENDPOINTS ADMINISTRATIVOS ---

@api_view(['POST'])
@permission_classes([AllowAny]) # Nota: Ajustar a IsAdministrador en producción
def admin_mark_paid(request, folio):
    """Fase 4: Registro manual de pago para finalizar el proceso del aspirante."""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    aspirante.pagado_status = True
    aspirante.status = 'ACEPTADO'
    aspirante.fase_actual = 5
    aspirante.fecha_pago = timezone.now()
    aspirante.recibido_por = request.data.get('admin_name', 'Admin')
    aspirante.metodo_pago = request.data.get('metodo_pago', 'Efectivo')
    aspirante.save()
    return Response({"message": "Pago registrado. Aspirante Aprobado.", "fase_actual": 5})

@api_view(['GET'])
@permission_classes([IsAdministrador])
def admin_view_document(request, folio, field_name):
    """Visor seguro para administradores. Desencripta documentos del estudiante o tutor."""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    
    # Referencias de campos por entidad
    student_fields = ['comprobante_domicilio', 'curp_pdf', 'acta_nacimiento_estudiante']
    tutor_fields = ['acta_nacimiento_tutor', 'curp_tutor_pdf']
    
    target_obj, target_field = None, None
    
    if field_name in student_fields:
        target_obj, target_field = aspirante, field_name
    elif field_name in tutor_fields:
        tutor_rel = AdmissionTutorAspirante.objects.filter(aspirante=aspirante).first()
        if tutor_rel:
            target_obj = tutor_rel.tutor
            target_field = 'acta_nacimiento' if field_name == 'acta_nacimiento_tutor' else 'curp_pdf'
    
    if not target_obj or not target_field or not hasattr(target_obj, target_field):
        return Response({"error": "Campo no válido o tutor no asociado"}, status=status.HTTP_400_BAD_REQUEST)
    
    file_field = getattr(target_obj, target_field)
    if not file_field:
        return Response({"error": "No hay archivo cargado"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        decrypted_content = decrypt_data(file_field.read())
        content_type = "application/pdf" if file_field.name.endswith(".pdf") else "application/octet-stream"
        return HttpResponse(decrypted_content, content_type=content_type)
    except Exception as e:
        return Response({"error": f"Error al desencriptar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
