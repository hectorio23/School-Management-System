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
    grupo_str = str(inscripcion.group) if (inscripcion and hasattr(inscripcion, 'group') and inscripcion.group) else \
                str(inscripcion.grupo) if (inscripcion and inscripcion.grupo) else "Pendiente de asignación"
    ciclo_str = inscripcion.ciclo_escolar.nombre if (inscripcion and inscripcion.ciclo_escolar) else "N/A"
    
    data = {
        "nombre": f"{estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}".upper(),
        "matricula": str(estudiante.matricula),
        "ciclo": ciclo_str,
        "grupo": grupo_str.upper(),
        "fecha": timezone.now().strftime('%d/%m/%Y')
    }
    
    buffer = fill_pdf_form(template_path, data)
    
    if not buffer:
        # Fallback simple
        buffer = io.BytesIO()
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(buffer)
        c.drawString(100, 750, f"CARTA REINSCRIPCION - {data['nombre']}")
        c.save()
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
