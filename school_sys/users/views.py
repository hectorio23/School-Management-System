from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone

from estudiantes.models import (
    Estudiante, 
    Tutor, 
    EstadoEstudiante, 
    HistorialEstadosEstudiante,
    Estrato,
    EvaluacionSocioeconomica
)
from pagos.models import (
    Pago,
    Adeudo,
    ConfiguracionPago,
    DiaNoHabil,
    ConceptoPago
)
from comedor.models import MenuSemanal, AsistenciaCafeteria
from .serializers_admin import (
    TutorSerializer, 
    EstudianteAdminSerializer, 
    EstudianteUpdateSerializer, 
    PagoSerializer,
    EstratoSerializer, 
    EvaluacionSocioeconomicaSerializer,
    EvaluacionAprobacionSerializer,
    BajaEstudianteSerializer,
    ConfiguracionPagoSerializer,
    DiaNoHabilSerializer,
    MenuSemanalSerializer,
    AsistenciaCafeteriaSerializer,
    AdeudoSerializer
)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class LargePagination(PageNumberPagination):
    page_size = 150
    page_size_query_param = 'page_size'
    max_page_size = 500


# ==========================================================================
# TUTORS
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_tutor_list(request):
    """
    GET: Lista paginada de tutores (150/página)
    POST: Crear nuevo tutor
    """
    if request.method == 'GET':
        tutors = Tutor.objects.all().order_by('apellido_paterno')
        paginator = LargePagination()
        result_page = paginator.paginate_queryset(tutors, request)
        serializer = TutorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_tutor_detail(request, pk):
    """
    GET: Detalle de un tutor
    PUT: Actualizar tutor
    DELETE: Eliminar tutor
    """
    tutor = get_object_or_404(Tutor, pk=pk)

    if request.method == 'GET':
        serializer = TutorSerializer(tutor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TutorSerializer(tutor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tutor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# STUDENTS
# ===========================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_student_list(request):
    """
    GET: Lista paginada de estudiantes (60/página)
    POST: Crear nuevo estudiante (transaccional: User + Estudiante)
    """
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 60
        
        # Optimizamos queries con select_related para evitar N+1 en grupo/grado
        students = Estudiante.objects.select_related('grupo', 'grupo__grado').order_by('matricula')
        result_page = paginator.paginate_queryset(students, request)

        data = []
        for s in result_page:
            # Manejo seguro de atributos nulos
            nombre_grado = "S/A"
            nombre_grupo = "S/A"
            
            if s.grupo:
                nombre_grupo = s.grupo.nombre
                if s.grupo.grado:
                    nombre_grado = f"{s.grupo.grado.nombre} {s.grupo.grado.nivel}"

            estrato = s.get_estrato_actual()
            estrato_nombre = estrato.nombre if estrato else "Sin Asignar"
            
            estado = s.get_estado_actual()
            estatus_nombre = estado.nombre if estado else "Sin Estado"

            data.append({
                "matricula": s.matricula,
                "apellido_paterno": s.apellido_paterno,
                "apellido_materno": s.apellido_materno,
                "nombres": s.nombre, 
                "grado": nombre_grado,
                "grupo": nombre_grupo,
                "estrato": estrato_nombre,
                "estatus": estatus_nombre,
            })
            
        return paginator.get_paginated_response(data)

    elif request.method == 'POST':
        serializer = EstudianteAdminSerializer(data=request.data)
        if serializer.is_valid():
            estudiante = serializer.save()
            return Response({"matricula": estudiante.matricula}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_student_detail(request, pk):
    """
    GET: Detalle completo de un estudiante (info personal, tutores, historial, evaluaciones)
    PUT: Actualizar campos del estudiante
    DELETE: Soft delete - Set status to 'Baja'
    """
    if request.method == 'GET':
        try:
            student = Estudiante.objects.select_related('grupo', 'grupo__grado', 'usuario').get(matricula=pk)
        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # info basica
        info_basica = {
            "matricula": student.matricula,
            "nombre_completo": f"{student.nombre} {student.apellido_paterno} {student.apellido_materno}",
            "nombres": student.nombre,
            "apellido_paterno": student.apellido_paterno,
            "apellido_materno": student.apellido_materno,
            "curp": student.usuario.username,
            "email": student.usuario.email,
            "direccion": student.direccion,
            "grupo": str(student.grupo) if student.grupo else "Sin Grupo",
            "grado": str(student.grupo.grado) if (student.grupo and student.grupo.grado) else "Sin Grado",
        }

        # tutores
        tutores_rel = student.estudiantetutor_set.select_related('tutor').all()
        tutores_data = []
        for rel in tutores_rel:
            t = rel.tutor
            tutores_data.append({
                "id": t.id,
                "nombre": f"{t.nombre} {t.apellido_paterno} {t.apellido_materno}",
                "telefono": t.telefono,
                "correo": t.correo,
                "parentesco": rel.parentesco,
                "activo": rel.activo
            })

        # historial
        historial_estados = student.historialestadosestudiante_set.select_related('estado').order_by('-fecha_creacion')
        estados_data = []
        for h in historial_estados:
            estados_data.append({
                "estado": h.estado.nombre,
                "fecha": h.fecha_creacion,
                "justificacion": h.justificacion
            })

        # evals socioeconomicas
        evaluaciones = student.evaluacionsocioeconomica_set.select_related('estrato').order_by('-fecha_evaluacion')
        evaluaciones_data = []
        for eva in evaluaciones:
            evaluaciones_data.append({
                "fecha": eva.fecha_evaluacion,
                "estrato_resultante": eva.estrato.nombre if eva.estrato else "Pendiente/Nulo",
                "ingreso_mensual": eva.ingreso_mensual,
                "aprobado": eva.aprobado
            })

        # resumen
        estrato_actual = student.get_estrato_actual()
        estado_actual = student.get_estado_actual()
        balance = student.get_balance_total()

        data = {
            "informacion_personal": info_basica,
            "resumen_academico": {
                "estrato_actual": estrato_actual.nombre if estrato_actual else "N/A",
                "estado_escolar": estado_actual.nombre if estado_actual else "N/A",
                "balance_adeudo": balance
            },
            "tutores": tutores_data,
            "historial_estados": estados_data,
            "evaluaciones_historico": evaluaciones_data,
            "metadata": {
                "usuario_id": student.usuario.id,
                "role": student.usuario.role,
                "activo_sistema": student.usuario.activo
            }
        }
        return Response(data)

    elif request.method == 'PUT':
        student = get_object_or_404(Estudiante, matricula=pk)
        serializer = EstudianteUpdateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Soft delete: Set status to 'Baja'
        student = get_object_or_404(Estudiante, matricula=pk)
        
        # Buscar estado 'Baja'
        try:
            # Intentar encontrar un estado que contenga 'Baja'
            estado_baja = EstadoEstudiante.objects.filter(nombre__icontains='Baja').first()
            if not estado_baja:
                 return Response({"error": "No existe un estado de 'Baja' configurado en el sistema"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Crear registro en historial
            HistorialEstadosEstudiante.objects.create(
                estudiante=student,
                estado=estado_baja,
                justificacion="Baja administrativa por eliminación"
            )
            
            # Opcional: Desactivar usuario
            student.usuario.activo = False
            student.usuario.save()

            return Response({"message": f"Estudiante dado de baja. Nuevo estado: {estado_baja.nombre}"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# PAYMENTS
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_pago_list(request):
    """
    GET: Lista paginada de pagos (50/página)
    POST: Crear nuevo pago
    """
    if request.method == 'GET':
        pagos = Pago.objects.all().order_by('-fecha_pago')
        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(pagos, request)
        serializer = PagoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = PagoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_pago_detail(request, pk):
    """
    GET: Detalle de un pago
    PUT: Actualizar pago
    DELETE: BLOQUEADO - Los pagos no se pueden eliminar
    """
    pago = get_object_or_404(Pago, pk=pk)

    if request.method == 'GET':
        serializer = PagoSerializer(pago)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PagoSerializer(pago, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        return Response(
            {"detail": "La eliminación de pagos no está permitida. Use cancelaciones o ajustes."}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


# ----- ESTRATOS -----


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_estrato_list(request):
    """listar o crear estratos"""
    if request.method == 'GET':
        estratos = Estrato.objects.all().order_by('nombre')
        serializer = EstratoSerializer(estratos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # mayusculas
        data = request.data.copy()
        for field in ['nombre', 'descripcion']:
            if field in data and data[field]:
                data[field] = str(data[field]).upper()
        
        serializer = EstratoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_estrato_detail(request, pk):
    """detalle, update o desactivar estrato"""
    estrato = get_object_or_404(Estrato, pk=pk)
    
    if request.method == 'GET':
        serializer = EstratoSerializer(estrato)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data.copy()
        for field in ['nombre', 'descripcion']:
            if field in data and data[field]:
                data[field] = str(data[field]).upper()
        
        serializer = EstratoSerializer(estrato, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # no eliminar, solo desactivar
        estrato.activo = False
        estrato.save()
        return Response({"detail": "Estrato desactivado"})


# ----- EVALUACIONES SOCIOECONOMICAS -----

@api_view(['GET'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_evaluacion_list(request):
    """listar evaluaciones pendientes"""
    pendientes = request.query_params.get('pendientes', 'true')
    
    if pendientes.lower() == 'true':
        evaluaciones = EvaluacionSocioeconomica.objects.filter(aprobado__isnull=True)
    else:
        evaluaciones = EvaluacionSocioeconomica.objects.all()
    
    evaluaciones = evaluaciones.select_related('estudiante', 'estrato', 'estrato_sugerido').order_by('-fecha_evaluacion')
    paginator = StandardPagination()
    result_page = paginator.paginate_queryset(evaluaciones, request)
    serializer = EvaluacionSocioeconomicaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_evaluacion_aprobar(request, pk):
    """aprobar/rechazar evaluacion"""
    evaluacion = get_object_or_404(EvaluacionSocioeconomica, pk=pk)
    serializer = EvaluacionAprobacionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    evaluacion.aprobado = data['aprobado']
    evaluacion.comentarios_comision = data.get('comentarios_comision', '').upper()
    evaluacion.fecha_aprobacion = timezone.now()
    
    if data['aprobado'] and data.get('estrato_id'):
        evaluacion.estrato_id = data['estrato_id']
    
    evaluacion.notificacion_enviada = False  # pendiente de notificar
    evaluacion.save()
    
    return Response({"detail": "Evaluacion actualizada", "aprobado": evaluacion.aprobado})


# ----- BAJAS -----

@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_estudiante_baja(request, pk):
    """dar de baja a estudiante"""
    estudiante = get_object_or_404(Estudiante, matricula=pk)
    serializer = BajaEstudianteSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    fecha_baja = data.get('fecha_baja', date.today())
    
    # buscar estado de baja
    tipo_baja = "BAJA TEMPORAL" if data['es_temporal'] else "BAJA DEFINITIVA"
    estado_baja = EstadoEstudiante.objects.filter(nombre__icontains='Baja').first()
    
    if not estado_baja:
        return Response({"error": "No existe estado de baja configurado"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # historial
    historial = HistorialEstadosEstudiante.objects.create(
        estudiante=estudiante,
        estado=estado_baja,
        justificacion=f"{tipo_baja}: {data['justificacion']}".upper(),
        fecha_baja=fecha_baja,
        es_baja_temporal=data['es_temporal']
    )
    
    # sumar adeudos pendientes
    adeudos_pendientes = Adeudo.objects.filter(
        estudiante=estudiante,
        estatus__in=['pendiente', 'vencido']
    )
    
    total_adeudo = adeudos_pendientes.aggregate(total=Sum('monto_total'))['total'] or 0
    
    # desactivar usuario
    estudiante.usuario.activo = False
    estudiante.usuario.save()
    
    return Response({
        "detail": f"Estudiante dado de baja: {tipo_baja}",
        "fecha_baja": fecha_baja,
        "adeudos_pendientes": float(total_adeudo),
        "cantidad_adeudos": adeudos_pendientes.count()
    })


# ----- ADEUDOS -----

@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_generar_adeudos_mensuales(request):
    """generar adeudos del mes para estudiantes activos"""
    from django.db import transaction
    
    # mes a generar
    mes_str = request.data.get('mes')  # formato: 2024-01
    if mes_str:
        try:
            year, month = map(int, mes_str.split('-'))
            mes = date(year, month, 1)
        except:
            return Response({"error": "Formato de mes invalido, usar YYYY-MM"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        hoy = date.today()
        mes = date(hoy.year, hoy.month, 1)
    
    # obtener configuracion
    config = ConfiguracionPago.objects.filter(activo=True).first()
    if not config:
        return Response({"error": "No hay configuracion de pago activa"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # obtener concepto de colegiatura
    concepto = ConceptoPago.objects.filter(nombre__icontains='COLEGIATURA', activo=True).first()
    if not concepto:
        return Response({"error": "No existe concepto de COLEGIATURA activo"}, status=status.HTTP_400_BAD_REQUEST)
    
    # estudiantes activos
    estudiantes_activos = Estudiante.objects.filter(usuario__activo=True)
    
    creados = 0
    errores = []
    
    with transaction.atomic():
        for est in estudiantes_activos:
            # verificar si ya tiene adeudo para este mes
            existe = Adeudo.objects.filter(
                estudiante=est,
                concepto=concepto,
                mes_correspondiente=mes
            ).exists()
            
            if existe:
                continue
            
            # calcular descuento por estrato
            estrato = est.get_estrato_actual()
            descuento = Decimal('0')
            if estrato:
                descuento = concepto.monto_base * (estrato.porcentaje_descuento / 100)
            
            monto_final = concepto.monto_base - descuento
            
            # fecha vencimiento: dia 10 del mes
            fecha_venc = date(mes.year, mes.month, config.dia_fin_ordinario)
            
            Adeudo.objects.create(
                estudiante=est,
                concepto=concepto,
                monto_base=concepto.monto_base,
                descuento_aplicado=descuento,
                monto_total=monto_final,
                fecha_vencimiento=fecha_venc,
                mes_correspondiente=mes,
                generado_automaticamente=True
            )
            creados += 1
    
    return Response({
        "detail": f"Adeudos generados para {mes.strftime('%B %Y')}",
        "creados": creados,
        "total_estudiantes": estudiantes_activos.count()
    })


@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_aplicar_recargos(request):
    """aplicar recargos a adeudos vencidos"""
    config = ConfiguracionPago.objects.filter(activo=True).first()
    if not config:
        return Response({"error": "No hay configuracion de pago activa"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    hoy = date.today()
    
    # adeudos vencidos sin recargo y no exentos
    adeudos_vencidos = Adeudo.objects.filter(
        fecha_vencimiento__lt=hoy,
        estatus='pendiente',
        recargo_aplicado=0,
        recargo_exento=False
    )
    
    aplicados = 0
    for adeudo in adeudos_vencidos:
        # 10% + $125
        monto_neto = adeudo.monto_base - adeudo.descuento_aplicado
        recargo = (monto_neto * config.porcentaje_recargo / 100) + config.monto_fijo_recargo
        
        adeudo.recargo_aplicado = recargo
        adeudo.monto_total = monto_neto + recargo
        adeudo.estatus = 'vencido'
        adeudo.save()
        aplicados += 1
    
    return Response({
        "detail": f"Recargos aplicados",
        "adeudos_afectados": aplicados
    })


@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_exentar_recargo(request, pk):
    """quitar recargo con justificacion"""
    adeudo = get_object_or_404(Adeudo, pk=pk)
    justificacion = request.data.get('justificacion', '')
    
    if not justificacion:
        return Response({"error": "Se requiere justificacion"}, status=status.HTTP_400_BAD_REQUEST)
    
    adeudo.recargo_exento = True
    adeudo.justificacion_exencion = justificacion.upper()
    
    # quitar recargo
    if adeudo.recargo_aplicado > 0:
        adeudo.monto_total = adeudo.monto_total - adeudo.recargo_aplicado
        adeudo.recargo_aplicado = 0
    
    adeudo.save()
    
    return Response({"detail": "Recargo exentado", "nuevo_total": float(adeudo.monto_total)})


@api_view(['GET'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_adeudos_vencidos(request):
    """adeudos vencidos"""
    adeudos = Adeudo.objects.filter(
        estatus__in=['vencido', 'pendiente'],
        fecha_vencimiento__lt=date.today()
    ).select_related('estudiante', 'concepto').order_by('fecha_vencimiento')
    
    paginator = StandardPagination()
    result_page = paginator.paginate_queryset(adeudos, request)
    serializer = AdeudoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# ----- CONFIGURACION PAGOS -----

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_configuracion_pago(request):
    """config de pagos"""
    config = ConfiguracionPago.objects.filter(activo=True).first()
    
    if request.method == 'GET':
        if not config:
            return Response({"detail": "No hay configuracion activa"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConfiguracionPagoSerializer(config)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if not config:
            config = ConfiguracionPago()
        serializer = ConfiguracionPagoSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----- COMEDOR -----

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_menu_semanal_list(request):
    """menus semanales"""
    if request.method == 'GET':
        menus = MenuSemanal.objects.filter(activo=True)
        serializer = MenuSemanalSerializer(menus, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MenuSemanalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_comedor_asistencia(request):
    """asistencia al comedor"""
    fecha_inicio = request.query_params.get('desde')
    fecha_fin = request.query_params.get('hasta')
    
    asistencias = AsistenciaCafeteria.objects.select_related('estudiante', 'menu')
    
    if fecha_inicio:
        asistencias = asistencias.filter(fecha_asistencia__gte=fecha_inicio)
    if fecha_fin:
        asistencias = asistencias.filter(fecha_asistencia__lte=fecha_fin)
    
    asistencias = asistencias.order_by('-fecha_asistencia')
    paginator = StandardPagination()
    result_page = paginator.paginate_queryset(asistencias, request)
    serializer = AsistenciaCafeteriaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_alumnos_alergias(request):
    """alumnos con alergias"""
    estudiantes = Estudiante.objects.filter(
        alergias_alimentarias__isnull=False,
        usuario__activo=True
    ).exclude(alergias_alimentarias='')
    
    data = []
    for est in estudiantes:
        data.append({
            "matricula": est.matricula,
            "nombre": f"{est.nombre} {est.apellido_paterno}".upper(),
            "grupo": str(est.grupo) if est.grupo else "SIN GRUPO",
            "alergias": est.alergias_alimentarias
        })
    
    return Response(data)


# ----- REPORTES -----

@api_view(['GET'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_reporte_ingresos_estrato(request):
    """ingresos agrupados por estrato"""
    from django.db.models import Count
    
    # pagos agrupados por estrato del estudiante
    estratos = Estrato.objects.filter(activo=True)
    resultado = []
    
    for estrato in estratos:
        # estudiantes con este estrato
        evaluaciones = EvaluacionSocioeconomica.objects.filter(
            estrato=estrato,
            aprobado=True
        ).values_list('estudiante_id', flat=True)
        
        total_pagado = Pago.objects.filter(
            adeudo__estudiante__in=evaluaciones
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        resultado.append({
            "estrato": estrato.nombre,
            "color": estrato.color,
            "total_pagado": float(total_pagado),
            "estudiantes": len(set(evaluaciones))
        })
    
    return Response(resultado)


@api_view(['GET'])
@permission_classes([AllowAny])  # cambiar a IsAdminUser despues de testing
def admin_reporte_recaudacion(request):
    """recaudacion ordinaria vs recargos"""
    # totales de adeudos
    adeudos = Adeudo.objects.all()
    
    total_base = adeudos.aggregate(total=Sum('monto_base'))['total'] or 0
    total_descuentos = adeudos.aggregate(total=Sum('descuento_aplicado'))['total'] or 0
    total_recargos = adeudos.aggregate(total=Sum('recargo_aplicado'))['total'] or 0
    total_pagado = adeudos.aggregate(total=Sum('monto_pagado'))['total'] or 0
    
    return Response({
        "monto_base_total": float(total_base),
        "descuentos_aplicados": float(total_descuentos),
        "recargos_aplicados": float(total_recargos),
        "total_pagado": float(total_pagado),
        "por_cobrar": float(total_base - total_descuentos + total_recargos - total_pagado)
    })
