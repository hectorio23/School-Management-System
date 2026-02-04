"""
Vistas para el endpoint de información del estudiante.
Refactorizado a Function Based Views (FBV) con decoradores.
"""
import os
from datetime import timedelta, date, datetime
from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pagos.models import Adeudo, Pago
from .models import Estudiante, Tutor, EstudianteTutor, EvaluacionSocioeconomica, Estrato
from .permissions import IsEstudiante
from .utils_pdf import generar_carta_reinscripcion, generar_carta_baja
from .serializers import (
    EstudianteInfoSerializer, TutorUpdateSerializer, 
    EstudioSocioeconomicoCreateSerializer, EstudianteAdeudoDetalleSerializer
)


"""Aqui es donde va la direccón del dashboard en caso de que 
   no se use un framework para el manejo de Front-End. 
   los html irán en la carpeta llamada templates/
   los recursos de css y javascript, van en la carpeta static
   en sus respectivos lugares
"""
def dashboard(request):
    
    # return render(request, "dashboars de estudiante")
    return render(request, "./dashboard.html")


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEstudiante]) 
def estudiante_info_view(request):
    """
    GET /students/info/
    
    Retorna la información del estudiante autenticado.
    Solo accesible para usuarios con rol 'estudiante'.
    """

    print(request.user)

    try:
        # Obtener el perfil de estudiante del usuario autenticado
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {"error": "No se encontró el perfil de estudiante asociado a este usuario."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = EstudianteInfoSerializer(estudiante)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsEstudiante])
def tutores_update_view(request):
    """
    PUT /students/tutores/
    
    Actualiza la información de todos los tutores del estudiante autenticado.
    Recibe un array de tutores con su información actualizada.
    Solo puede actualizar tutores que pertenezcan al estudiante.
    """
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {"error": "No se encontró el perfil de estudiante asociado a este usuario."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    tutores_data = request.data.get('tutores', [])

    for tutor in tutores_data:
        if not all(tutor):
            return Response(
                { "error": "Campos incompletos." },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if not isinstance(tutores_data, list):
        return Response(
            {"error": "Se esperaba un array de tutores en el campo 'tutores'."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not tutores_data:
        return Response(
            {"error": "Debe proporcionar al menos un tutor para actualizar."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener IDs de tutores que pertenecen al estudiante
    tutores_permitidos = set(
        EstudianteTutor.objects.filter(
            estudiante=estudiante,
            activo=True
        ).values_list('tutor_id', flat=True)
    )
    
    errores = []
    tutores_actualizados = []
    
    for idx, tutor_data in enumerate(tutores_data):
        tutor_id = tutor_data.get('tutor_id') or tutor_data.get('id')
        
        if not tutor_id:
            errores.append({
                "index": idx,
                "error": "Falta el campo 'tutor_id'."
            })
            continue
        
        # Verificar que el tutor pertenezca al estudiante
        if tutor_id not in tutores_permitidos:
            errores.append({
                "index": idx,
                "tutor_id": tutor_id,
                "error": "No tienes permiso para actualizar este tutor."
            })
            continue
        
        try:
            tutor = Tutor.objects.get(id=tutor_id)
        except Tutor.DoesNotExist:
            errores.append({
                "index": idx,
                "tutor_id": tutor_id,
                "error": "Tutor no encontrado."
            })
            continue
        
        serializer = TutorUpdateSerializer(tutor, data=tutor_data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            tutores_actualizados.append(serializer.data)
        else:
            errores.append({
                "index": idx,
                "tutor_id": tutor_id,
                "errors": serializer.errors
            })
    
    if errores:
        return Response({
            "message": "Algunos tutores no pudieron ser actualizados por información incompleta.",
            "actualizados": tutores_actualizados,
            "errores": errores
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        "message": "Todos los tutores proporcionados fueron actualizados correctamente.",
        "tutores": tutores_actualizados
    }, status=status.HTTP_200_OK)


def guardar_documentos_extra(estudiante, files):
    """
    Función placeholder para guardar documentos extra (Acta, CURP).
    Será implementada posteriormente.
    """
    # TODO: Implementar lógica de guardado de documentos
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEstudiante])
def create_estudio_socioeconomico_view(request):
    """
    POST /students/estudio-socioeconomico/
    
    Crea una nueva evaluación socioeconómica para el estudiante.
    
    Validaciones:
    - Tiempo mínimo entre estudios (configurado en MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES)
    - Cambios de estrato > 2 niveles requieren aprobación especial
    
    Calcula el estrato automáticamente basado en el ingreso mensual (Cambiar en producción):
    - Ingreso <= 10,000 -> Estrato B
    - Ingreso > 10,000 -> Estrato A
    """
    
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {"error": "No se encontró el perfil de estudiante asociado a este usuario."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Validar tiempo desde último estudio
    meses_requeridos = int(os.getenv('MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES', '1'))
    fecha_limite = timezone.now() - timedelta(days=30 * meses_requeridos)
    
    ultimo_estudio = EvaluacionSocioeconomica.objects.filter(
        estudiante=estudiante,
        fecha_evaluacion__gte=fecha_limite
    ).first()
    
    if ultimo_estudio:
        dias_restantes = (ultimo_estudio.fecha_evaluacion + timedelta(days=30 * meses_requeridos) - timezone.now()).days
        return Response({
            "error": f"Debe esperar {meses_requeridos} mes(es) entre estudios socioeconómicos.",
            "ultimo_estudio": ultimo_estudio.fecha_evaluacion.strftime("%Y-%m-%d"),
            "dias_restantes": max(0, dias_restantes)
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = EstudioSocioeconomicoCreateSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        
        # Calcular Estrato sugerido
        ingreso = validated_data.get('ingreso_mensual')
        
        # Definir rangos de estrato por ingreso
        # TODO: Esto debería venir de la tabla Estrato o configuración
        if ingreso <= 5000:
            nombre_estrato = 'C'
        elif ingreso <= 10000:
            nombre_estrato = 'B'
        else:
            nombre_estrato = 'A'
        
        try:
            estrato_sugerido = Estrato.objects.get(nombre=nombre_estrato)
        except Estrato.DoesNotExist:
            # Fallback: buscar el primer estrato activo
            estrato_sugerido = Estrato.objects.filter(activo=True).first()
            if not estrato_sugerido:
                return Response(
                    {"error": f"El estrato '{nombre_estrato}' no está configurado en el sistema."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # Detectar cambio grande de estrato (> 2 niveles)
        requiere_aprobacion_especial = False
        estrato_actual = estudiante.get_estrato_actual()
        
        if estrato_actual:
            # Mapeo de estratos a niveles numéricos para comparación
            niveles = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
            nivel_actual = niveles.get(estrato_actual.nombre, 0)
            nivel_nuevo = niveles.get(estrato_sugerido.nombre, 0)
            
            diferencia = abs(nivel_actual - nivel_nuevo)
            if diferencia > 2:
                requiere_aprobacion_especial = True
            
        # Extraer archivos para procesarlos aparte
        acta = validated_data.pop('acta_nacimiento', None)
        curp = validated_data.pop('curp', None)

        ## Guardar archivos
        # TODO: Hacer función que gestione el almacenamiento de los archivos
        # por cada estudiante
        
        # files_to_save = {}
        # if acta:
        #     files_to_save['acta_nacimiento'] = acta
        # if curp:
        #     files_to_save['curp'] = curp
            
        # if files_to_save:
        #     guardar_documentos_extra(estudiante, files_to_save)
            
        # Crear evaluación
        evaluacion = EvaluacionSocioeconomica.objects.create(
            estudiante=estudiante,
            estrato=None if requiere_aprobacion_especial else estrato_sugerido,  # No asignar si requiere aprobación
            estrato_sugerido=estrato_sugerido,
            ingreso_mensual=ingreso,
            tipo_vivienda=validated_data.get('tipo_vivienda'),
            miembros_hogar=validated_data.get('miembros_hogar'),
            documentos_json='{}',  # JSON vacío por defecto
            requiere_aprobacion_especial=requiere_aprobacion_especial,
            aprobado=None if requiere_aprobacion_especial else True,  # Pendiente si requiere aprobación
            # Guardar snapshot del porcentaje de descuento al momento de la evaluación
            porcentaje_descuento_snapshot=estrato_sugerido.porcentaje_descuento if estrato_sugerido else None
        )
        
        response_data = {
            "message": "Evaluación socioeconómica registrada correctamente.",
            "estrato_sugerido": estrato_sugerido.nombre,
            "requiere_aprobacion_especial": requiere_aprobacion_especial,
        }
        
        if requiere_aprobacion_especial:
            response_data["NOTA"] = "El cambio de estrato es significativo (más de 2 niveles). Requiere aprobación del administrador."
        else:
            response_data["NOTA"] = "El administrador tiene que validar el Estrato socioeconómico"
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEstudiante])
def download_carta_reinscripcion(request):
    """Permite al estudiante descargar su carta de reinscripción."""
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response({"error": "No se encontró el perfil de estudiante"}, status=status.HTTP_404_NOT_FOUND)
    
    buffer = generar_carta_reinscripcion(estudiante)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reinscripcion_{estudiante.matricula}.pdf"'
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEstudiante])
def download_carta_baja(request):
    """Permite al estudiante descargar su carta de baja con desglose financiero."""
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response({"error": "No se encontró el perfil de estudiante"}, status=status.HTTP_404_NOT_FOUND)
        
    buffer = generar_carta_baja(estudiante)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="baja_{estudiante.matricula}.pdf"'
    return response


# =============================================================================
# FINANCIAL FEATURES (RF-CTA-02, RF-CAL-04, RF-PAG-01)
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEstudiante])
def student_payments_history(request):
    """
    GET /students/pagos/historial/
    Retorna el historial completo de adeudos y pagos del estudiante.
    RF-CTA-02
    """
    try:
        estudiante = request.user.perfil_estudiante
    except Estudiante.DoesNotExist:
        return Response({"error": "Perfil de estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    adeudos = Adeudo.objects.filter(estudiante=estudiante).select_related('concepto').prefetch_related('pago_set').order_by('-fecha_vencimiento')
    
    serializer = EstudianteAdeudoDetalleSerializer(adeudos, many=True)
    
    resumen = {
        "balance_total": estudiante.get_balance_total(),
        "adeudos": serializer.data
    }
    return Response(resumen)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEstudiante])
def student_payment_simulator(request):
    """
    POST /students/pagos/simular/
    Calcula cuánto tendría que pagar el estudiante si pagara en una fecha futura.
    RF-CAL-04
    Body: { "adeudo_id": 1, "fecha_pago": "2024-12-15" }
    """
    adeudo_id = request.data.get('adeudo_id')
    fecha_str = request.data.get('fecha_pago')
    
    if not adeudo_id or not fecha_str:
        return Response({"error": "Se requiere adeudo_id y fecha_pago (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # Parse fecha (puede venir como datetime o date string)
        fecha_simulada = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        estudiante = request.user.perfil_estudiante
        adeudo = Adeudo.objects.get(id=adeudo_id, estudiante=estudiante)
    except (Estudiante.DoesNotExist, Adeudo.DoesNotExist):
        return Response({"error": "Adeudo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if adeudo.estatus == 'pagado':
         return Response({"mensaje": "Este adeudo ya está pagado."}, status=status.HTTP_200_OK)

    # --- Lógica de Simulación (Replicando Adeudo.save logic pero sin guardar) ---
    monto_base = adeudo.monto_base
    descuento = adeudo.descuento_aplicado
    monto_con_descuento = max(Decimal('0.00'), monto_base - descuento)
    
    recargo_simulado = Decimal('0.00')
    vencimiento = adeudo.fecha_vencimiento 
    if isinstance(vencimiento, datetime):
        vencimiento = vencimiento.date()
        
    # Si la fecha simulada es posterior al vencimiento
    if fecha_simulada > vencimiento:
        if not adeudo.recargo_exento:
             # Recargo Fijo + 10%
             pct_recargo = Decimal('0.10')
             fijo_recargo = Decimal('125.00')
             recargo_simulado = (monto_con_descuento * pct_recargo) + fijo_recargo
             
    total_simulado = monto_con_descuento + recargo_simulado
    
    return Response({
        "adeudo_id": adeudo.id,
        "concepto": adeudo.concepto.nombre,
        "fecha_vencimiento": vencimiento,
        "fecha_simulada": fecha_simulada,
        "desglose": {
            "monto_base": monto_base,
            "descuento": descuento,
            "recargo_estimado": recargo_simulado,
            "subtotal_antes_recargo": monto_base - descuento if descuento else monto_base # Fix for walrus not supported in some python versions if < 3.8, safer to just repeat
        },
        "total_a_pagar": total_simulado
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEstudiante])
def student_upload_receipt(request):
    """
    POST /students/pagos/subir-comprobante/
    Permite subir un comprobante de pago para validación manual.
    RF-PAG-01
    Multipart Form: 
      - adeudo_id: int
      - comprobante: file
      - metodo_pago: str (Transferencia, Deposito)
      - referencia: str
    """
    return Response({"message": "Feature pending due to storage configuration"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    # try:
    #     estudiante = request.user.perfil_estudiante
    # except Estudiante.DoesNotExist:
    #     return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    # adeudo_id = request.data.get('adeudo_id')
    # archivo = request.FILES.get('comprobante')
    # metodo = request.data.get('metodo_pago', 'Transferencia')
    # referencia = request.data.get('referencia', '')
    
    # if not adeudo_id or not archivo:
    #     return Response({"error": "Falta adeudo_id o el archivo del comprobante"}, status=status.HTTP_400_BAD_REQUEST)
        
    # adeudo = get_object_or_404(Adeudo, id=adeudo_id, estudiante=estudiante)
    
    # # Validar si ya está pagado
    # if adeudo.estatus == 'pagado':
    #     return Response({"error": "Este adeudo ya está marcado como pagado"}, status=status.HTTP_400_BAD_REQUEST)
        
    # # Crear Pago con flag de "Por Validar" (o método específico)
    # # Nota: El modelo Pago no tiene campo 'validado', usaremos 'notas' para marcarlo o un método especial.
    # # Si queremos ser estrictos, deberíamos añadir un campo bool 'verificado' al modelo Pago.
    # # Por ahora, lo pondremos en notas.
    
    # # Guardar archivo (Falta lógica de storage real, django lo maneja en media/)
    # # Simulamos ruta
    # ruta_ficticia = f"comprobantes/{estudiante.matricula}/{archivo.name}"
    
    # # En un entorno real: default_storage.save(ruta_ficticia, archivo)
    
    # pago = Pago.objects.create(
    #     adeudo=adeudo,
    #     monto=adeudo.monto_total - adeudo.monto_pagado, # Asumimos pago total del saldo
    #     metodo_pago=f"{metodo} (POR VALIDAR)",
    #     numero_referencia=referencia,
    #     ruta_recibo=ruta_ficticia,
    #     notas=f"Pago subido por estudiante el {timezone.now()}. Pendiente de validación administrativa.",
    #     recibido_por="Portal Estudiante"
    # )
    
    # return Response({
    #     "message": "Comprobante subido correctamente. Su pago entrará en proceso de validación (24-48 hrs).",
    #     "pago_id": pago.id,
    #     "estatus": "En Revisión"
    # }, status=status.HTTP_201_CREATED)
