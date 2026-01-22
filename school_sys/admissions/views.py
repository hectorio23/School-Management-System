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
    RegisterAspiranteSerializer,
    AdmissionUserSerializer,
    AspirantePhase1Serializer
)

# --- AUTH ENDPOINTS ---

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_send_code(request):
    """
    Envia código de verificación al correo.
    Simulado: Retorna el código en la respuesta para pruebas.
    """
    serializer = VerificationCodeSerializer(data=request.data)
    if serializer.is_valid():
        verification = serializer.save()
        # TODO: Integrar envío de email real aquí
        return Response({
            "message": "Código enviado (Simulado)",
            "email": verification.email,
            "code_debug": verification.code # Solo para desarrollo
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_verify_code(request):
    """
    Verifica el código recibido.
    """
    serializer = VerifyCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        
        try:
            verification = VerificationCode.objects.get(
                email=email, 
                code=code, 
                is_verified=False
            )
            
            if not verification.is_valid():
                return Response({"error": "Código expirado"}, status=status.HTTP_400_BAD_REQUEST)
            
            verification.is_verified = True
            verification.save()
            return Response({"message": "Correo verificado exitosamente"}, status=status.HTTP_200_OK)
            
        except VerificationCode.DoesNotExist:
            return Response({"error": "Código inválido o correo no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_aspirante(request):
    """
    Registra un nuevos usuario y aspirante.
    Requiere que el correo haya sido verificado previamente.
    """
    # 1. Validar correo verificado
    if 'user_data' not in request.data or 'email' not in request.data['user_data']:
         return Response({"error": "Faltan datos de usuario (user_data)"}, status=status.HTTP_400_BAD_REQUEST)
         
    email = request.data['user_data']['email']
    
    # Check si tiene verificacion valida reciente (ej. ultimos 30 min)
    is_verified = VerificationCode.objects.filter(
        email=email, 
        is_verified=True, 
        created_at__gte=timezone.now() - timezone.timedelta(minutes=30)
    ).exists()
    
    if not is_verified:
        return Response({"error": "El correo no ha sido verificado o la verificación expiró"}, status=status.HTTP_403_FORBIDDEN)
        
    # 2. Registrar
    serializer = RegisterAspiranteSerializer(data=request.data)
    if serializer.is_valid():
        aspirante = serializer.save()
        
        # Invalidar código usado
        VerificationCode.objects.filter(email=email).delete()
        
        return Response({
            "message": "Cuenta creada exitosamente. Pase a Fase 1.",
            "folio": aspirante.user.folio,
            "email": aspirante.user.email
        }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
         
    # Archivos
    if 'comprobante_domicilio' in request.FILES:
        aspirante.comprobante_domicilio = request.FILES['comprobante_domicilio']
    
    # Checks
    aspirante.aceptacion_reglamento = request.data.get('aceptacion_reglamento', str(aspirante.aceptacion_reglamento)).lower() == 'true'
    aspirante.autorizacion_imagen = request.data.get('autorizacion_imagen', str(aspirante.autorizacion_imagen)).lower() == 'true'
    
    if not (aspirante.aceptacion_reglamento and aspirante.autorizacion_imagen):
        return Response({"error": "Debe aceptar el reglamento y la autorización de imagen"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Marcar otros checks como entregados (en este flujo simplificado)
    aspirante.acta_nacimiento_check = True
    aspirante.curp_check = True
    
    if aspirante.fase_actual == 3: aspirante.fase_actual = 4
    aspirante.save()
    return Response({"message": "Fase 3 OK. Pendiente de Pago.", "fase_actual": aspirante.fase_actual})

# --- ADMIN ENDPOINTS ---

@api_view(['POST'])
@permission_classes([AllowAny]) # Debería ser IsAdminUser
def admin_mark_paid(request, folio):
    """Fase 4: Registrar Pago (Solo Admin)"""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    aspirante.pagado_status = True
    aspirante.status = 'aprobado'
    aspirante.fase_actual = 5
    aspirante.fecha_pago = timezone.now()
    aspirante.recibido_por = request.data.get('admin_name', 'Admin')
    aspirante.metodo_pago = request.data.get('metodo_pago', 'Efectivo')
    aspirante.save()
    return Response({"message": "Pago registrado. Aspirante Aprobado.", "fase_actual": 5})
