"""
1. Llenado de Solicitud de Preingreso
    - Por favor guarde el código que se le asigna al final con el 
    objetivo de identificar su trámite de forma ágil y segura.

2. Análisis de Solicitudes
    - La tercera semana de febrero el Comité de Admisiones sesiona 
    para determinar las solicitudes que avanzan a la siguiente fase.

3. Agenda para Visita Domiciliaria
    - La cuarta semana de febrero el Departamento de Trabajo Social 
    se comunica vía telefónica para agendar día y hora de la visita domiciliaria.

4. Visita Domiciliaria
    - Se realiza la visita por Trabajo Social en la primera 
    quincena de marzo.

5. Entrevista con Psicología Educativa
    - Se realiza la entrevista de Psicología Educativa la primera 
    quincena de marzo, posterior a la visita domiciliaria. 
    Este proceso contempla la aplicación de instrumentos de evaluación.

6. Aplicación de exámenes pedagógicos
    - El alumno solicitante se presenta a realizar la evaluación 
    pedagógica en la fecha que le sea asignada al concluir la entrevista 
    en Psicología Educativa.

7. Valoración y análisis de aspirantes
    - El Comité de Admisiones sesiona para valorar cada caso.

8. Publicación de Resultados
    - Con base en el análisis del Comité de Admisiones, se publicará el 
    viernes 23 de mayo a partir de las 7:30 a.m. en los diferentes accesos del 
    Centro Educativo una lista de los alumnos aceptados.

9. Reunión con Padres de Familia
    - Se citará vía telefónica a las familias que son aceptadas al 
    Centro Educativo para la Primera Reunión Informativa.
"""


import os
import json
import mimetypes
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password

from users.permissions import IsAdministrador, CanManageAdmisiones
from .permissions import IsAspirante
from .authentication import AdmissionJWTAuthentication
from dateutil.relativedelta import relativedelta
from users.models import User
from estudiantes.models import (
    Estudiante, Tutor, EstudianteTutor, EstadoEstudiante,
    HistorialEstadosEstudiante, CicloEscolar, Grupo, Grado, NivelEducativo
)
from django.test import RequestFactory
from .utils_security import decrypt_data
from .models import VerificationCode, AdmissionUser, Aspirante, AdmissionTutor, AdmissionTutorAspirante
from .utils_pdf import generar_contrato_servicios
from django.core.mail import send_mail
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
        # TODO: Remove this line on production!
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- ENDPOINTS DE FASES DE ADMISIÓN ---

@api_view(['GET'])
@authentication_classes([AdmissionJWTAuthentication])
@permission_classes([IsAuthenticated, IsAspirante])
def aspirante_dashboard(request, folio):
    """
    Endpoint para el dashboard del estudiante.
    Retorna información detallada y notificaciones dinámicas basadas en fechas.
    """
    if request.user.folio != folio:
        return Response({"error": "Acceso denegado"}, status=status.HTTP_403_FORBIDDEN)

    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    
    # El usuario solicita restringir la información detallada hasta la fase 4
    if aspirante.fase_actual < 4:
        return Response({
            "fase_actual": aspirante.fase_actual,
            "status": aspirante.status,
            "message": "Complete las fases anteriores para ver más información."
        })

    # Datos base (Aspirante + Tutores)
    serializer = AspirantePhase1Serializer(aspirante)
    data = serializer.data
    
    # Añadir campos administrativos y de proceso
    data.update({
        'fase_actual': aspirante.fase_actual,
        'status': aspirante.status,
        'direccion': aspirante.direccion,
        'curp': aspirante.curp,
        'nivel_ingreso': aspirante.nivel_ingreso,
    })

    # Lógica de Notificaciones Dinámicas
    now = timezone.now()
    today = now.date()
    notification = {
        "active": False,
        "type": None,
        "message": "Espere los resultados",
        "date": None
    }

    # Jerarquía: Examen > Entrevista > Visita
    # Solo se muestran si la fecha no ha pasado (expirado)
    
    if aspirante.fecha_examen_pedagogico and aspirante.fecha_examen_pedagogico >= today:
        notification.update({
            "active": True,
            "type": "EXAMEN_PEDAGOGICO",
            "message": "Fecha para aplicar examen pedagógico",
            "date": aspirante.fecha_examen_pedagogico
        })
    elif aspirante.fecha_entrevista_psicologia and aspirante.fecha_entrevista_psicologia >= today:
        notification.update({
            "active": True,
            "type": "ENTREVISTA_PSICOLOGIA",
            "message": "Fecha de entrevista psicológica",
            "date": aspirante.fecha_entrevista_psicologia
        })
    elif aspirante.fecha_visita_domiciliaria and aspirante.fecha_visita_domiciliaria.date() >= today:
        notification.update({
            "active": True,
            "type": "VISITA_DOMICILIARIA",
            "message": "Fecha de visita domiciliaria",
            "date": aspirante.fecha_visita_domiciliaria
        })

    data['notificacion'] = notification
    
    # Lista de documentos requeridos para la visita domiciliaria (mostrar en fase 4+)
    data['documentos_requeridos'] = {
        "mensaje": "Favor de contar con los siguientes documentos a la mano:",
        "documentos": [
            {
                "nombre": "Comprobante de domicilio",
                "descripcion": "Con tres meses de vigencia y que coincida con la credencial del INE"
            },
            {
                "nombre": "Fotografía de la fachada del domicilio",
                "descripcion": "Fotografía clara del domicilio del aspirante"
            },
            {
                "nombre": "Comprobante de ingresos",
                "descripcion": "Recibo de nómina o formato proporcionado por la institución"
            },
            {
                "nombre": "Carta de Ingresos",
                "descripcion": "En caso de no contar con recibo de nómina, descargar y completar esta carta",
                "descarga_url": "/api/admission/templates/carta_ingresos/"
            },
            {
                "nombre": "Credencial del INE",
                "descripcion": "Credencial del INE de los padres de familia o tutores"
            },
            {
                "nombre": "Contrato de arrendamiento o recibo de predial",
                "descripcion": "Documento que acredite la propiedad o arrendamiento del domicilio"
            },
            {
                "nombre": "Carta bajo protesta",
                "descripcion": "Descargar, completar y firmar esta carta",
                "descarga_url": "/api/admission/templates/carta_bajo_protesta/"
            }
        ]
    }
    
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
        return Response({
            "message": "Fase 1 OK", 
            "fase_actual": aspirante.fase_actual,
            "data": AspirantePhase1Serializer(aspirante).data
        })
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
    return Response({
        "message": "Fase 2 OK", 
        "fase_actual": aspirante.fase_actual,
        "data": AspirantePhase1Serializer(aspirante).data # Reusamos serializer para devolver info completa
    })

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
                # 1. Documentos del aspirante (Aspirante model)
                student_docs = [
                    'curp_pdf', 'acta_nacimiento', 'foto_credencial', 
                    'boleta_ciclo_anterior', 'boleta_ciclo_actual'
                ]
                for field in student_docs:
                    if field in request.FILES:
                        setattr(aspirante, field, request.FILES[field])
                
                # 2. Documentos de los tutores (AdmissionTutor model)
                tutor_rels = AdmissionTutorAspirante.objects.filter(aspirante=aspirante)
                if not tutor_rels.exists():
                     return Response({"error": "Debe registrar al menos un tutor en la Fase 1"}, status=status.HTTP_400_BAD_REQUEST)

                tutor_file_map = {
                    'acta_nacimiento_tutor': 'acta_nacimiento',
                    'comprobante_domicilio_tutor': 'comprobante_domicilio',
                    'foto_fachada_domicilio': 'foto_fachada_domicilio',
                    'comprobante_ingresos': 'comprobante_ingresos',
                    'carta_ingresos': 'carta_ingresos',
                    'ine_tutor': 'ine_tutor',
                    'contrato_arrendamiento_predial': 'contrato_arrendamiento_predial',
                    'carta_bajo_protesta': 'carta_bajo_protesta',
                    'curp_pdf_tutor': 'curp_pdf'
                }

                for rel in tutor_rels:
                    tutor = rel.tutor
                    tutor_updated = False
                    
                    for req_field, model_field in tutor_file_map.items():
                        # Buscamos archivos específicos o genéricos
                        specific_field = f"tutor_{tutor.id}_{req_field}"
                        file_obj = None
                        
                        if specific_field in request.FILES:
                            file_obj = request.FILES[specific_field]
                        elif req_field in request.FILES and tutor_rels.count() == 1:
                            file_obj = request.FILES[req_field]
                        
                        if file_obj:
                            setattr(tutor, model_field, file_obj)
                            tutor_updated = True
                        else:
                            # Verificar si ya existe el archivo en el modelo (si es una actualización parcial)
                            existing_file = getattr(tutor, model_field)
                            if not existing_file:
                                return Response({
                                    "error": f"El documento '{req_field}' es obligatorio para el tutor {tutor.nombre}"
                                }, status=status.HTTP_400_BAD_REQUEST)
                    
                    if tutor_updated:
                        tutor.save()

                serializer.save()
                
                # Actualización de validaciones internas (aspirante)
                if aspirante.acta_nacimiento: aspirante.acta_nacimiento_check = True
                if aspirante.curp_pdf: aspirante.curp_check = True
                
                if aspirante.fase_actual == 3: 
                    aspirante.fase_actual = 4
                    # Notificar por correo
                    try:
                        send_mail(
                            subject="Confirmación de Inscripción - Proceso Completado",
                            message=f"Hola {aspirante.nombre},\n\nHas completado exitosamente el proceso de inscripción (Fase 3).\nTu solicitud ha pasado a la fase de validación final (Fase 4).\nPuedes descargar tu contrato de servicios educativos desde el dashboard.",
                            from_email=None,
                            recipient_list=[aspirante.user.email],
                            fail_silently=True,
                        )
                    except Exception:
                        pass
                
                aspirante.save()
            return Response({"message": "Fase 3 OK.", "fase_actual": aspirante.fase_actual})
        except Exception as e:
            return Response({"error": f"Error al procesar archivos: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([AdmissionJWTAuthentication])
@permission_classes([IsAuthenticated, IsAspirante])
def download_contrato(request, folio):
    """Permite al aspirante descargar su contrato de servicios educativos."""
    if request.user.folio != folio:
        return Response({"error": "No tienes permiso para descargar este documento"}, status=status.HTTP_403_FORBIDDEN)
    
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    buffer = generar_contrato_servicios(aspirante)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{folio}.pdf"'
    return response

# --- ENDPOINTS ADMINISTRATIVOS ---

@api_view(['POST'])
@permission_classes([AllowAny]) # Nota: Ajustar a IsAdministrador en producción
def admin_mark_paid(request, folio):
    """Fase 4: Registro manual de pago para finalizar el proceso del aspirante. (COMENTADO)"""
    # aspirante = get_object_or_404(Aspirante, user__folio=folio)
    # aspirante.pagado_status = True
    # aspirante.status = 'ACEPTADO'
    # aspirante.fase_actual = 5
    # aspirante.fecha_pago = timezone.now()
    # aspirante.recibido_por = request.data.get('admin_name', 'Admin')
    # aspirante.metodo_pago = request.data.get('metodo_pago', 'Efectivo')
    # aspirante.save()
    return Response({"message": "La fase de pago está deshabilitada temporalmente."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([CanManageAdmisiones])
def admin_view_document(request, folio, field_name):
    """Visor seguro para administradores. Desencripta documentos del estudiante o tutor."""
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    
    # Referencias de campos por entidad (Request keys)
    student_fields = [
        'curp_pdf', 'acta_nacimiento', 'foto_credencial', 
        'boleta_ciclo_anterior', 'boleta_ciclo_actual'
    ]
    tutor_fields_map = {
        'acta_nacimiento_tutor': 'acta_nacimiento',
        'comprobante_domicilio_tutor': 'comprobante_domicilio',
        'foto_fachada_domicilio': 'foto_fachada_domicilio',
        'comprobante_ingresos': 'comprobante_ingresos',
        'carta_ingresos': 'carta_ingresos',
        'ine_tutor': 'ine_tutor',
        'contrato_arrendamiento_predial': 'contrato_arrendamiento_predial',
        'carta_bajo_protesta': 'carta_bajo_protesta'
    }
    
    target_obj, target_field = None, None
    
    if field_name in student_fields:
        target_obj, target_field = aspirante, field_name
    elif field_name in tutor_fields_map:
        tutor_rel = AdmissionTutorAspirante.objects.filter(aspirante=aspirante).first()
        if tutor_rel:
            target_obj = tutor_rel.tutor
            target_field = tutor_fields_map[field_name]
    
    if not target_obj or not target_field or not hasattr(target_obj, target_field):
        return Response({"error": "Campo no válido o tutor no asociado"}, status=status.HTTP_400_BAD_REQUEST)
    
    file_field = getattr(target_obj, target_field)
    if not file_field:
        return Response({"error": "No hay archivo cargado"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        
        decrypted_content = decrypt_data(file_field.read())
        
        # Intentamos determinar el tipo MIME real basado en el nombre del archivo
        content_type, _ = mimetypes.guess_type(file_field.name)
        if not content_type:
            content_type = "application/octet-stream"
            
        return HttpResponse(decrypted_content, content_type=content_type)
    except Exception as e:
        return Response({"error": f"Error al desencriptar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([CanManageAdmisiones])
def admin_view_aspirante_document(request, folio, field_name):
    """
    Endpoint para que el administrador vea documentos del aspirante.
    Parámetros:
        - folio: ID del aspirante
        - field_name: Nombre del campo (curp_pdf, acta_nacimiento, foto_credencial, 
                      boleta_ciclo_anterior, boleta_ciclo_actual)
    """
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    
    allowed_fields = [
        'curp_pdf', 'acta_nacimiento', 'foto_credencial', 
        'boleta_ciclo_anterior', 'boleta_ciclo_actual'
    ]
    
    if field_name not in allowed_fields:
        return Response({
            "error": f"Campo no válido: {field_name}",
            "campos_permitidos": allowed_fields
        }, status=status.HTTP_400_BAD_REQUEST)
    
    file_field = getattr(aspirante, field_name, None)
    if not file_field:
        return Response({"error": "No hay archivo cargado para este campo"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        decrypted_content = decrypt_data(file_field.read())
        content_type, _ = mimetypes.guess_type(file_field.name)
        if not content_type:
            content_type = "application/octet-stream"
        return HttpResponse(decrypted_content, content_type=content_type)
    except Exception as e:
        return Response({"error": f"Error al desencriptar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([CanManageAdmisiones])
def admin_view_tutor_document(request, tutor_id, field_name):
    """
    Endpoint para que el administrador vea documentos del tutor por su ID.
    Parámetros:
        - tutor_id: ID del tutor
        - field_name: Nombre del campo (acta_nacimiento, curp_pdf, comprobante_domicilio,
                      foto_fachada_domicilio, comprobante_ingresos, carta_ingresos,
                      ine_tutor, contrato_arrendamiento_predial, carta_bajo_protesta)
    """
    tutor = get_object_or_404(AdmissionTutor, id=tutor_id)
    
    allowed_fields = [
        'acta_nacimiento', 'curp_pdf', 'comprobante_domicilio', 
        'foto_fachada_domicilio', 'comprobante_ingresos', 'carta_ingresos',
        'ine_tutor', 'contrato_arrendamiento_predial', 'carta_bajo_protesta'
    ]
    
    if field_name not in allowed_fields:
        return Response({
            "error": f"Campo no válido: {field_name}",
            "campos_permitidos": allowed_fields
        }, status=status.HTTP_400_BAD_REQUEST)
    
    file_field = getattr(tutor, field_name, None)
    if not file_field:
        return Response({"error": "No hay archivo cargado para este campo"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        decrypted_content = decrypt_data(file_field.read())
        content_type, _ = mimetypes.guess_type(file_field.name)
        if not content_type:
            content_type = "application/octet-stream"
        return HttpResponse(decrypted_content, content_type=content_type)
    except Exception as e:
        return Response({"error": f"Error al desencriptar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- ENDPOINTS PÚBLICOS ---

@api_view(['GET'])
@permission_classes([AllowAny])
def download_template(request, template_name):
    """
    Endpoint público para descargar plantillas de documentos.
    Parámetros:
        - template_name: 'carta_ingresos' o 'carta_bajo_protesta'
    """
    
    templates_map = {
        'carta_ingresos': 'cartas-de-ingresos-2025.pdf',
        'carta_bajo_protesta': 'cartas-bajo-protesta-2025.pdf',
    }
    
    if template_name not in templates_map:
        return Response({
            "error": f"Plantilla no válida: {template_name}",
            "plantillas_disponibles": list(templates_map.keys())
        }, status=status.HTTP_400_BAD_REQUEST)
    
    file_name = templates_map[template_name]
    file_path = os.path.join(settings.BASE_DIR, 'documents', file_name)
    
    if not os.path.exists(file_path):
        return Response({"error": "Archivo de plantilla no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    except Exception as e:
        return Response({"error": f"Error al leer archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- ENDPOINTS DE MIGRACIÓN DE ASPIRANTES ---

@api_view(['POST'])
@permission_classes([CanManageAdmisiones])
def migrate_aspirante_to_student(request, folio):
    """
    Migra un aspirante aceptado a estudiante.
    
    POST /api/admission/admin/<folio>/migrate/
    
    Validaciones:
    - Status: ACEPTADO
    - Fase actual: >= 4 (documentos completos)
    - Ciclo escolar activo (creado hace menos de 3 meses)
    - Grupo disponible con cupo (máx. 30 estudiantes)
    
    Proceso:
    1. Crear User con rol 'estudiante'
    2. Crear Estudiante con matrícula secuencial
    3. Crear/Reutilizar Tutor y vincular
    4. Asignar a grupo según nivel de ingreso
    """
    
    aspirante = get_object_or_404(Aspirante, user__folio=folio)
    
    # 1. Validar status
    if aspirante.status != 'ACEPTADO':
        return Response({
            "error": f"El aspirante debe tener status 'ACEPTADO'. Status actual: {aspirante.status}"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. Validar fase (documentos completos)
    if aspirante.fase_actual < 4:
        return Response({
            "error": f"El aspirante debe completar al menos la fase 4. Fase actual: {aspirante.fase_actual}"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 3. Validar ciclo escolar activo (menos de 3 meses)
    fecha_limite = timezone.now().date() - relativedelta(months=3)
    ciclo_activo = CicloEscolar.objects.filter(
        activo=True,
        fecha_inicio__gte=fecha_limite
    ).first()
    
    if not ciclo_activo:
        return Response({
            "error": "No hay ciclo escolar activo o el ciclo actual tiene más de 3 meses. "
                     "No se pueden aceptar nuevos estudiantes."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 4. Buscar grupo disponible según nivel de ingreso
    nivel_ingreso = aspirante.nivel_ingreso  # Ej: "1ro de Primaria"
    
    # Parsear nivel e identificar grado
    grupo_asignado = None
    grupos_disponibles = Grupo.objects.filter(
        grado__nivel__nombre__icontains=nivel_ingreso.split()[-1] if nivel_ingreso else 'Primaria'
    ).order_by('nombre')
    
    for grupo in grupos_disponibles:
        estudiantes_en_grupo = Estudiante.objects.filter(grupo=grupo).count()
        if estudiantes_en_grupo < 30:  # Máximo 30 estudiantes por grupo
            grupo_asignado = grupo
            break
    
    if not grupo_asignado:
        return Response({
            "error": f"No hay grupos disponibles con cupo para el nivel: {nivel_ingreso}"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # 5. Crear User para el estudiante
            email = aspirante.user.email
            # Generar username basado en email
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            
            # Obtener password original (hasheado) del AdmissionUser
            user = User.objects.create(
                username=username,
                email=email,
                password=aspirante.user.password,  # Ya está hasheado
                role='estudiante',
                is_active=True
            )
            
            # 6. Obtener/Crear estado "Activo"
            estado_activo, _ = EstadoEstudiante.objects.get_or_create(
                nombre='Activo',
                defaults={
                    'descripcion': 'Estudiante inscrito y activo',
                    'es_estado_activo': True
                }
            )
            
            # 7. Crear Estudiante
            estudiante = Estudiante.objects.create(
                usuario=user,
                nombre=aspirante.nombre.upper(),
                apellido_paterno=aspirante.apellido_paterno.upper(),
                apellido_materno=aspirante.apellido_materno.upper(),
                direccion=aspirante.direccion or 'PENDIENTE',
                curp=aspirante.curp,
                fecha_nacimiento=aspirante.fecha_nacimiento,
                sexo=aspirante.sexo,
                telefono=aspirante.telefono,
                escuela_procedencia=aspirante.escuela_procedencia,
                grupo=grupo_asignado
            )
            
            # 8. Crear historial de estado inicial
            HistorialEstado.objects.create(
                estudiante=estudiante,
                estado=estado_activo,
                justificacion='Inscripción por admisión'
            )
            
            # 9. Migrar tutores (reutilizar si existe por email/curp)
            tutores_admision = AdmissionTutorAspirante.objects.filter(aspirante=aspirante)
            tutores_creados = []
            
            for rel in tutores_admision:
                tutor_adm = rel.tutor
                
                # Buscar tutor existente por email
                tutor_existente = None
                if tutor_adm.correo:
                    tutor_existente = Tutor.objects.filter(correo=tutor_adm.correo).first()
                
                if tutor_existente:
                    tutor = tutor_existente
                else:
                    # Crear nuevo tutor
                    tutor = Tutor.objects.create(
                        nombre=tutor_adm.nombre.upper(),
                        apellido_paterno=tutor_adm.apellido_paterno.upper(),
                        apellido_materno=tutor_adm.apellido_materno.upper() if tutor_adm.apellido_materno else '',
                        telefono=tutor_adm.telefono or '',
                        correo=tutor_adm.correo or '',
                        parentesco=rel.parentesco
                    )
                
                # Vincular tutor con estudiante
                EstudianteTutor.objects.create(
                    estudiante=estudiante,
                    tutor=tutor,
                    parentesco=rel.parentesco,
                    es_principal=(len(tutores_creados) == 0)  # Primer tutor es principal
                )
                tutores_creados.append(tutor.id)
            
            # 10. Actualizar aspirante
            aspirante.status = 'MIGRADO'
            aspirante.save()
            
            return Response({
                "message": "Aspirante migrado exitosamente a estudiante",
                "estudiante": {
                    "matricula": estudiante.matricula,
                    "nombre_completo": f"{estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}",
                    "grupo": str(grupo_asignado),
                    "email": user.email,
                    "username": user.username
                },
                "tutores_vinculados": tutores_creados
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            "error": f"Error al migrar aspirante: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([CanManageAdmisiones])
def migrate_all_accepted(request):
    """
    Migra todos los aspirantes con status 'ACEPTADO' a estudiantes.
    
    POST /api/admission/admin/migrate-all/
    
    Body opcional:
    {
        "nivel_ingreso": "Primaria"  // Filtrar por nivel
    }
    
    Retorna lista de aspirantes migrados y errores.
    """
    nivel_filter = request.data.get('nivel_ingreso')
    
    aspirantes = Aspirante.objects.filter(status='ACEPTADO', fase_actual__gte=4)
    if nivel_filter:
        aspirantes = aspirantes.filter(nivel_ingreso__icontains=nivel_filter)
    
    resultados = {
        "migrados": [],
        "errores": [],
        "total_procesados": 0
    }
    
    for aspirante in aspirantes:
        resultados["total_procesados"] += 1
        
        # Simulamos la llamada al endpoint individual
        try:
            # Creamos un pseudo-request
            factory = RequestFactory()
            pseudo_request = factory.post(f'/api/admission/admin/{aspirante.user.folio}/migrate/')
            pseudo_request.user = request.user
            pseudo_request.data = {}
            
            response = migrate_aspirante_to_student(pseudo_request, aspirante.user.folio)
            
            if response.status_code == 201:
                resultados["migrados"].append({
                    "folio": aspirante.user.folio,
                    "nombre": f"{aspirante.nombre} {aspirante.apellido_paterno}",
                    "matricula": response.data.get("estudiante", {}).get("matricula")
                })
            else:
                resultados["errores"].append({
                    "folio": aspirante.user.folio,
                    "nombre": f"{aspirante.nombre} {aspirante.apellido_paterno}",
                    "error": response.data.get("error", "Error desconocido")
                })
        except Exception as e:
            resultados["errores"].append({
                "folio": aspirante.user.folio,
                "nombre": f"{aspirante.nombre} {aspirante.apellido_paterno}",
                "error": str(e)
            })
    
    return Response({
        "message": f"Proceso de migración completado",
        "resumen": {
            "total_procesados": resultados["total_procesados"],
            "migrados_exitosamente": len(resultados["migrados"]),
            "con_errores": len(resultados["errores"])
        },
        "detalle": resultados
    }, status=status.HTTP_200_OK)

