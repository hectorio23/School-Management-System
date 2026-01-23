from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import VerificationCode, AdmissionUser, Aspirante
from .serializers import (
    VerificationCodeSerializer, 
    VerifyCodeSerializer, 
    AspiranteRegistrationSerializer,
    AspirantePhase1Serializer,
    AspirantePhase3Serializer
)
import json

# --- AUTH ENDPOINTS ---

@api_view(['POST'])
@permission_classes([AllowAny])
def register_initiate(request):
    """
    Paso 1: Recibe datos y envía código al correo.
    """
    serializer = AspiranteRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if email exists
        if AdmissionUser.objects.filter(email=email).exists():
            return Response({"error": "El correo ya está registrado"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Almacenar datos en JSON
        data_json = json.dumps(serializer.validated_data)
        
        v_serializer = VerificationCodeSerializer(data={"email": email})
        if v_serializer.is_valid():
            verification = v_serializer.save(data_json=data_json)
            return Response({
                "message": "Código enviado. Tiene 1 minuto para confirmar.",
                "email": email,
                "code_debug": verification.code # Solo para desarrollo
            }, status=status.HTTP_201_CREATED)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_confirm(request):
    """
    Paso 2: Verifica código y crea la cuenta + aspirante.
    """
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response({"error": "Faltan email o código"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        verification = VerificationCode.objects.get(email=email, code=code, is_verified=False)
        
        if not verification.is_valid():
             return Response({"error": "Código expirado o inválido"}, status=status.HTTP_400_BAD_REQUEST)
             
        # Crear cuenta
        data = json.loads(verification.data_json)
        
        from django.contrib.auth.hashers import make_password
        
        from django.db import transaction
        with transaction.atomic():
            user = AdmissionUser.objects.create(
                email=data['email'],
                password=make_password(data['password']),
                is_verified=True
            )
            aspirante = Aspirante.objects.create(
                user=user,
                nombre=data['nombre'],
                apellido_paterno=data['apellido_paterno'],
                apellido_materno=data['apellido_materno'],
                curp=data['curp']
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

# --- PHASES ENDPOINTS ---

@api_view(['GET'])
@permission_classes([AllowAny])
def aspirante_me(request, folio):
    """
    Retorna la información actual del aspirante por folio.
    """
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    serializer = AspirantePhase1Serializer(aspirante)
    data = serializer.data
    data['fase_actual'] = aspirante.fase_actual
    data['status'] = aspirante.status
    data['pagado_status'] = aspirante.pagado_status
    return Response(data)

@api_view(['PUT'])
@permission_classes([AllowAny])
def aspirante_phase1(request, folio):
    """Fase 1: Datos Personales y Tutores"""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    serializer = AspirantePhase1Serializer(aspirante, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Fase 1 OK", "fase_actual": aspirante.fase_actual})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny])
def aspirante_phase2(request, folio):
    """Fase 2: Socioeconómico"""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    if aspirante.fase_actual < 2:
         return Response({"error": "Complete Fase 1"}, status=status.HTTP_400_BAD_REQUEST)
    
    fields = ['ingreso_mensual_familiar', 'ocupacion_padre', 'ocupacion_madre', 'tipo_vivienda', 'miembros_hogar', 'vehiculos', 'internet_encasa']
    for f in fields:
        if f in request.data: setattr(aspirante, f, request.data[f])
    
    if aspirante.fase_actual == 2: aspirante.fase_actual = 3
    aspirante.save()
    return Response({"message": "Fase 2 OK", "fase_actual": aspirante.fase_actual})

@api_view(['PUT'])
@permission_classes([AllowAny])
def aspirante_phase3(request, folio):
    """Fase 3: Documentación y Legal"""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    if aspirante.fase_actual < 3:
         return Response({"error": "Complete Fase 2"}, status=status.HTTP_400_BAD_REQUEST)
         
    serializer = AspirantePhase3Serializer(aspirante, data=request.data, partial=True)
    if serializer.is_valid():
        # Manejo de archivos si vienen en FILES
        for field in ['comprobante_domicilio', 'curp_pdf', 'acta_nacimiento_estudiante', 'acta_nacimiento_tutor', 'curp_tutor_pdf']:
            if field in request.FILES:
                setattr(aspirante, field, request.FILES[field])
        
        serializer.save()
        
        # Marcar checks como verdaderos si se enviaron (el serializer valida aceptacion)
        # Suponemos que si sube el archivo, el check se marca (o se marca manual)
        if aspirante.acta_nacimiento_estudiante: aspirante.acta_nacimiento_check = True
        if aspirante.curp_pdf: aspirante.curp_check = True
        
        if aspirante.fase_actual == 3: 
            aspirante.fase_actual = 4
        
        aspirante.save()
        return Response({"message": "Fase 3 OK. Pendiente de Pago.", "fase_actual": aspirante.fase_actual})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- ADMIN ENDPOINTS ---

@api_view(['POST'])
@permission_classes([AllowAny]) # Debería ser IsAdminUser
def admin_mark_paid(request, folio):
    """Fase 4: Registrar Pago (Solo Admin)"""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    aspirante.pagado_status = True
    aspirante.status = 'ACEPTADO'
    aspirante.fase_actual = 5
    aspirante.fecha_pago = timezone.now()
    aspirante.recibido_por = request.data.get('admin_name', 'Admin')
    aspirante.metodo_pago = request.data.get('metodo_pago', 'Efectivo')
    aspirante.save()
    return Response({"message": "Pago registrado. Aspirante Aprobado.", "fase_actual": 5})
