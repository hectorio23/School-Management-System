import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.utils import timezone
from django.conf import settings
from pypdf import PdfReader, PdfWriter

from pypdf.generic import NameObject

def fill_pdf_form(template_path, data):
    """Llena los campos de un formulario PDF (AcroForms) con los datos proporcionados."""
    if not os.path.exists(template_path):
        return None

    try:
        reader = PdfReader(template_path)
        writer = PdfWriter()

        # Copiamos las páginas
        writer.append_pages_from_reader(reader)

        # Importante: pypdf a veces necesita que copiemos manualmente el AcroForm
        # para que update_page_form_field_values funcione en el writer.
        if "/AcroForm" in reader.trailer["/Root"]:
            writer.root_object.update({
                NameObject("/AcroForm"): reader.trailer["/Root"]["/AcroForm"]
            })

        # Rellenar los campos
        writer.update_page_form_field_values(writer.pages[0], data)

        buffer = io.BytesIO()
        writer.write(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error al llenar formulario PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def generar_contrato_servicios(aspirante):
    """Genera un archivo PDF con el contrato de servicios educativos inyectando datos en la plantilla."""
    template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'pdfs', 'contrato_base.pdf')
    
    nombre_completo = f"{aspirante.nombre} {aspirante.apellido_paterno} {aspirante.apellido_materno}".upper()
    folio_str = str(aspirante.user.folio)
    nivel_str = str(aspirante.nivel_ingreso or 'N/A').upper()
    fecha_str = timezone.now().strftime('%d/%m/%Y')
    
    data = {
        "nombre": nombre_completo,
        "folio": folio_str,
        "nivel_ingreso": nivel_str,
        "fecha": fecha_str
    }
    
    buffer = fill_pdf_form(template_path, data)
    
    if not buffer:
        buffer = _generar_contrato_programatico(aspirante, nombre_completo, folio_str, nivel_str, fecha_str)
        
    return buffer


def _generar_contrato_programatico(aspirante, nombre_completo, folio_str, nivel_str, fecha_str):
    """Genera un contrato de servicios educativos completo con ReportLab (sin plantilla externa)."""
    from .models import AdmissionTutorAspirante
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ContratoTitle', parent=styles['Title'], fontSize=14, spaceAfter=6)
    subtitle_style = ParagraphStyle('ContratoSubtitle', parent=styles['Heading2'], fontSize=11, spaceAfter=4)
    body_style = ParagraphStyle('ContratoBody', parent=styles['Normal'], fontSize=9, leading=13, spaceAfter=4)
    clause_style = ParagraphStyle('ContratoClause', parent=styles['Normal'], fontSize=9, leading=13, spaceAfter=6, leftIndent=20)
    bold_style = ParagraphStyle('ContratoBold', parent=body_style, fontName='Helvetica-Bold')
    center_style = ParagraphStyle('ContratoCenter', parent=body_style, alignment=1)
    
    # --- ENCABEZADO ---
    elements.append(Paragraph("CONTRATO DE PRESTACIÓN DE SERVICIOS EDUCATIVOS", title_style))
    elements.append(Paragraph(f"Ciclo Escolar Vigente", center_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # --- DATOS DEL CONTRATO ---
    elements.append(Paragraph("I. DATOS DE IDENTIFICACIÓN", subtitle_style))
    
    info_data = [
        ["Folio:", folio_str, "Fecha:", fecha_str],
        ["Alumno(a):", nombre_completo, "Nivel:", nivel_str],
        ["CURP:", aspirante.curp or 'N/A', "Teléfono:", aspirante.telefono or 'N/A'],
    ]
    info_table = Table(info_data, colWidths=[1*inch, 2.5*inch, 0.9*inch, 2.5*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.1*inch))
    
    # --- DATOS DEL TUTOR ---
    tutor_rel = AdmissionTutorAspirante.objects.filter(aspirante=aspirante).select_related('tutor').first()
    if tutor_rel:
        tutor = tutor_rel.tutor
        tutor_nombre = f"{tutor.nombre} {tutor.apellido_paterno} {tutor.apellido_materno or ''}".upper().strip()
        tutor_tel = tutor.numero_telefono or 'N/A'
        tutor_email = tutor.email or 'N/A'
        parentesco = tutor_rel.parentesco or 'Tutor'
    else:
        tutor_nombre, tutor_tel, tutor_email, parentesco = 'N/A', 'N/A', 'N/A', 'N/A'
    
    tutor_data = [
        ["Padre/Tutor:", tutor_nombre, "Parentesco:", parentesco],
        ["Teléfono:", tutor_tel, "Correo:", tutor_email],
    ]
    tutor_table = Table(tutor_data, colWidths=[1*inch, 2.5*inch, 0.9*inch, 2.5*inch])
    tutor_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(tutor_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # --- CLÁUSULAS ---
    elements.append(Paragraph("II. OBJETO DEL CONTRATO", subtitle_style))
    elements.append(Paragraph(
        f"El presente contrato tiene por objeto establecer los términos y condiciones bajo los cuales "
        f"la Institución Educativa prestará servicios educativos al alumno(a) <b>{nombre_completo}</b>, "
        f"en el nivel de <b>{nivel_str}</b>, durante el ciclo escolar vigente.", clause_style
    ))
    
    elements.append(Paragraph("III. OBLIGACIONES DE LA INSTITUCIÓN", subtitle_style))
    clausulas_inst = [
        "Proporcionar educación conforme a los planes y programas de estudio vigentes autorizados por la SEP.",
        "Garantizar un ambiente seguro y propicio para el aprendizaje.",
        "Informar oportunamente a los padres o tutores sobre el desempeño académico del alumno.",
        "Emitir la documentación oficial correspondiente al término del ciclo escolar.",
        "Brindar los servicios complementarios contratados (comedor, biblioteca, actividades extracurriculares).",
    ]
    for i, cl in enumerate(clausulas_inst, 1):
        elements.append(Paragraph(f"<b>{i}.</b> {cl}", clause_style))
    
    elements.append(Paragraph("IV. OBLIGACIONES DEL PADRE O TUTOR", subtitle_style))
    clausulas_tutor = [
        "Realizar el pago puntual de las colegiaturas dentro del período ordinario (del día 1 al 10 de cada mes).",
        "A partir del día 11 se aplicará un recargo del 10% sobre la colegiatura más un monto fijo de $125.00 MXN.",
        "Mantener actualizada la información de contacto y datos socioeconómicos del alumno.",
        "Cumplir con el reglamento escolar y apoyar las actividades educativas del alumno.",
        "Notificar por escrito cualquier baja temporal o definitiva del alumno.",
        "Acudir a las reuniones y citas programadas por la institución.",
    ]
    for i, cl in enumerate(clausulas_tutor, 1):
        elements.append(Paragraph(f"<b>{i}.</b> {cl}", clause_style))
    
    elements.append(Paragraph("V. CONDICIONES FINANCIERAS", subtitle_style))
    elements.append(Paragraph(
        "Las cuotas mensuales serán determinadas conforme al estrato socioeconómico asignado al alumno "
        "tras la evaluación correspondiente. La institución se reserva el derecho de solicitar la "
        "revalidación anual de dicha evaluación. Los descuentos por estrato y becas se aplicarán de "
        "forma secuencial: primero el descuento por estrato sobre el monto base, y posteriormente "
        "el porcentaje de beca sobre el monto ya estratificado.", clause_style
    ))
    
    elements.append(Paragraph("VI. VIGENCIA Y TERMINACIÓN", subtitle_style))
    elements.append(Paragraph(
        "El presente contrato tendrá vigencia durante el ciclo escolar en curso. Podrá darse por terminado "
        "anticipadamente por cualquiera de las partes mediante aviso por escrito con 15 días de anticipación. "
        "En caso de baja, la institución emitirá una constancia con el desglose financiero correspondiente. "
        "Los adeudos pendientes al momento de la baja serán congelados conforme a las políticas institucionales.",
        clause_style
    ))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # --- FIRMAS ---
    elements.append(Paragraph("VII. FIRMAS", subtitle_style))
    elements.append(Spacer(1, 0.4*inch))
    
    firma_data = [
        ["_" * 35, "", "_" * 35],
        [tutor_nombre, "", "Representante de la Institución"],
        ["Padre / Madre / Tutor", "", "Dirección General"],
    ]
    firma_table = Table(firma_data, colWidths=[2.8*inch, 1*inch, 2.8*inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(firma_table)
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Documento generado el {fecha_str}. Este contrato es válido con las firmas de ambas partes.", center_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
