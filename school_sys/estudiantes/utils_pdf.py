import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.utils import timezone
from django.conf import settings
from admissions.utils_pdf import fill_pdf_form

def generar_carta_reinscripcion(estudiante):
    """Genera un archivo PDF con la carta de reinscripción confirmada inyectando datos en la plantilla."""
    template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'pdfs', 'reinscripcion_base.pdf')
    
    # Obtener datos para la carta
    inscripcion = estudiante.inscripciones.filter(grupo__ciclo_escolar__activo=True).first()
    grupo_str = str(inscripcion.grupo) if (inscripcion and inscripcion.grupo) else "Pendiente de asignación"
    ciclo_str = inscripcion.ciclo_escolar.nombre if (inscripcion and hasattr(inscripcion, 'ciclo_escolar') and inscripcion.ciclo_escolar) else \
                (str(inscripcion.grupo.ciclo_escolar) if (inscripcion and inscripcion.grupo) else "N/A")
    
    nombre_completo = f"{estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}".upper()
    fecha_str = timezone.now().strftime('%d/%m/%Y')
    
    data = {
        "nombre": nombre_completo,
        "matricula": str(estudiante.matricula),
        "ciclo": ciclo_str,
        "grupo": grupo_str.upper(),
        "fecha": fecha_str
    }
    
    buffer = fill_pdf_form(template_path, data)
    
    if not buffer:
        buffer = _generar_carta_reinscripcion_programatica(estudiante, nombre_completo, data, inscripcion)
        
    return buffer


def _generar_carta_reinscripcion_programatica(estudiante, nombre_completo, data, inscripcion):
    """Genera carta de reinscripción completa con ReportLab (sin plantilla externa)."""
    from pagos.models import Adeudo, ConceptoPago
    from estudiantes.models import EstudianteTutor, Estrato
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.7*inch, bottomMargin=0.7*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ReinscTitle', parent=styles['Title'], fontSize=14, spaceAfter=6)
    header_style = ParagraphStyle('ReinscHeader', parent=styles['Heading2'], fontSize=11, spaceAfter=4)
    body_style = ParagraphStyle('ReinscBody', parent=styles['Normal'], fontSize=9, leading=13, spaceAfter=4)
    center_style = ParagraphStyle('ReinscCenter', parent=body_style, alignment=1)
    
    # --- ENCABEZADO ---
    elements.append(Paragraph("CARTA DE REINSCRIPCIÓN", title_style))
    elements.append(Paragraph("Ciclo Escolar Vigente", center_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # --- DATOS ---
    elements.append(Paragraph(f"<b>Fecha de emisión:</b> {data['fecha']}", body_style))
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("A quien corresponda:", body_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        f"Por medio de la presente, se confirma que el alumno(a) <b>{nombre_completo}</b>, "
        f"con matrícula <b>{data['matricula']}</b>, ha sido reinscrito(a) para continuar "
        f"sus estudios en esta Institución Educativa.", body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    # --- DATOS ACADÉMICOS ---
    elements.append(Paragraph("Datos Académicos", header_style))
    
    acad_data = [
        ["Matrícula:", data['matricula'], "Ciclo Escolar:", data['ciclo']],
        ["Grupo:", data['grupo'], "Nivel:", str(inscripcion.grupo.grado.nivel_educativo) if inscripcion and inscripcion.grupo else "N/A"],
        ["Grado:", str(inscripcion.grupo.grado) if inscripcion and inscripcion.grupo else "N/A", "", ""],
    ]
    acad_table = Table(acad_data, colWidths=[1.1*inch, 2.2*inch, 1.1*inch, 2.2*inch])
    acad_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(acad_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # --- CONDICIONES FINANCIERAS ---
    elements.append(Paragraph("Condiciones Financieras para el Ciclo", header_style))
    
    estrato = estudiante.get_estrato_actual()
    estrato_nombre = estrato.nombre if estrato else "Sin asignar"
    estrato_desc = f"{estrato.porcentaje_descuento}% de descuento" if estrato else "N/A"
    
    # Obtener concepto de colegiatura para el nivel
    cuota_base = "Consultar en Administración"
    try:
        nivel = inscripcion.grupo.grado.nivel_educativo if inscripcion and inscripcion.grupo else None
        if nivel:
            concepto_col = ConceptoPago.objects.filter(tipo_concepto='colegiatura', nivel_educativo=nivel, activo=True).first()
            if concepto_col:
                cuota_base = f"${concepto_col.monto_base:,.2f} MXN"
    except Exception:
        pass
    
    # Verificar becas
    becas_info = "Ninguna"
    try:
        from estudiantes.models import BecaEstudiante
        becas_activas = BecaEstudiante.objects.filter(estudiante=estudiante, activa=True)
        if becas_activas.exists():
            becas_info = ", ".join([f"{b.beca.nombre} ({b.beca.porcentaje_descuento}%)" for b in becas_activas])
    except Exception:
        pass
    
    fin_data = [
        ["Estrato socioeconómico:", f"{estrato_nombre} — {estrato_desc}"],
        ["Cuota base de colegiatura:", cuota_base],
        ["Becas activas:", becas_info],
        ["Período ordinario de pago:", "Del día 1 al 10 de cada mes"],
        ["Recargo por pago tardío:", "10% sobre cuota neta + $125.00 MXN fijo"],
    ]
    fin_table = Table(fin_data, colWidths=[2.2*inch, 4.5*inch])
    fin_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
    ]))
    elements.append(fin_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # --- TÉRMINOS ---
    elements.append(Paragraph("Términos de la Reinscripción", header_style))
    elements.append(Paragraph(
        "Al aceptar la reinscripción, el padre, madre o tutor se compromete a cumplir con el reglamento "
        "escolar vigente, a realizar los pagos de colegiaturas en tiempo y forma, y a mantener actualizada "
        "la información de contacto y datos socioeconómicos del alumno. La institución se reserva el "
        "derecho de solicitar la revalidación anual del estudio socioeconómico.", body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # --- FIRMAS ---
    # Obtener tutor principal
    tutor_nombre = "Padre / Madre / Tutor"
    try:
        rel = EstudianteTutor.objects.filter(estudiante=estudiante, activo=True, es_principal=True).select_related('tutor').first()
        if not rel:
            rel = EstudianteTutor.objects.filter(estudiante=estudiante, activo=True).select_related('tutor').first()
        if rel:
            t = rel.tutor
            tutor_nombre = f"{t.nombre} {t.apellido_paterno} {t.apellido_materno or ''}".upper().strip()
    except Exception:
        pass
    
    firma_data = [
        ["_" * 35, "", "_" * 35],
        [tutor_nombre, "", "Dirección General"],
        ["Padre / Madre / Tutor", "", "Institución Educativa"],
    ]
    firma_table = Table(firma_data, colWidths=[2.8*inch, 1*inch, 2.8*inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(firma_table)
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        f"Documento generado el {data['fecha']}. Esta carta es un comprobante de reinscripción "
        f"y no sustituye al contrato de servicios educativos.", center_style
    ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generar_carta_baja(estudiante):
    """Genera un archivo PDF con la carta de baja y el desglose financiero."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    header_style = styles['Heading2']
    body_style = styles['Normal']
    
    # Título
    elements.append(Paragraph("CONSTANCIA DE BAJA Y ESTADO DE CUENTA", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Datos Estudiante
    elements.append(Paragraph(f"Fecha: {timezone.now().strftime('%d/%m/%Y')}", body_style))
    elements.append(Paragraph(f"A quien corresponda:", body_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    texto_baja = f"""
    Por medio de la presente, se hace constar que el alumno <b>{estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}</b>, 
    con matrícula <b>{estudiante.matricula}</b>, ha causado baja de esta institución educativa.
    <br/><br/>
    A continuación se presenta el desglose financiero del estado de cuenta al momento de la baja:
    """
    elements.append(Paragraph(texto_baja, body_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de Adeudos/Pagos
    data = [["Concepto", "Monto Total", "Monto Pagado", "Saldo Pendiente", "Estatus"]]
    adeudos = estudiante.adeudo_set.all().order_by('fecha_vencimiento')
    
    total_pendiente = 0
    for a in adeudos:
        saldo = a.monto_total - a.monto_pagado
        total_pendiente += saldo
        data.append([
            a.concepto.nombre,
            f"${a.monto_total:,.2f}",
            f"${a.monto_pagado:,.2f}",
            f"${saldo:,.2f}",
            a.get_estatus_display()
        ])
    
    data.append(["TOTAL", "", "", f"${total_pendiente:,.2f}", ""])
    
    table = Table(data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))
    
    final_text = """
    Se informa que, de acuerdo con las políticas institucionales, los adeudos pendientes han sido congelados. 
    Cualquier aclaración posterior favor de acudir al departamento de finanzas.
    """
    elements.append(Paragraph(final_text, body_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generar_estado_cuenta_pdf(estudiante):
    """Genera un archivo PDF con el historial completo de adeudos y pagos."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    header_style = styles['Heading2']
    body_style = styles['Normal']
    
    # Header
    elements.append(Paragraph("ESTADO DE CUENTA ACADÉMICO", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    
    # info
    elements.append(Paragraph(f"<b>Estudiante:</b> {estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}", body_style))
    elements.append(Paragraph(f"<b>Matrícula:</b> {estudiante.matricula}", body_style))
    elements.append(Paragraph(f"<b>Fecha de Emisión:</b> {timezone.now().strftime('%d/%m/%Y %H:%M')}", body_style))
    elements.append(Spacer(1, 0.3 * inch))
    
    # Adeudos
    elements.append(Paragraph("Detalle de Adeudos y Pagos", header_style))
    elements.append(Spacer(1, 0.1 * inch))
    
    data = [["Fecha", "Concepto", "Total", "Pagado", "Saldo", "Estatus"]]
    adeudos = Adeudo.objects.filter(estudiante=estudiante).order_by('fecha_vencimiento', 'id')
    
    total_adeudado = 0
    total_pagado = 0
    
    for a in adeudos:
        saldo = a.monto_total - a.monto_pagado
        total_adeudado += a.monto_total
        total_pagado += a.monto_pagado
        
        data.append([
            a.fecha_generacion.strftime('%d/%m/%y') if a.fecha_generacion else 'N/A',
            a.concepto.nombre[:30],
            f"${a.monto_total:,.2f}",
            f"${a.monto_pagado:,.2f}",
            f"${saldo:,.2f}",
            a.get_estatus_display()
        ])
    
    # Totales row
    data.append([
        "TOTALES", 
        "", 
        f"${total_adeudado:,.2f}", 
        f"${total_pagado:,.2f}", 
        f"${total_adeudado - total_pagado:,.2f}", 
        ""
    ])
    
    table = Table(data, colWidths=[0.8*inch, 2.2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (4,-1), (4,-1), colors.red),
    ]))
    
    elements.append(table)
    
    # Mensaje final
    elements.append(Spacer(1, 0.5 * inch))
    balance_text = f"<b>Balance Pendiente Total: ${estudiante.get_balance_total():,.2f}</b>"
    elements.append(Paragraph(balance_text, ParagraphStyle('Balance', parent=body_style, fontSize=12, alignment=1)))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
