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
    
    data = {
        "nombre": f"{aspirante.nombre} {aspirante.apellido_paterno} {aspirante.apellido_materno}".upper(),
        "folio": str(aspirante.user.folio),
        "nivel_ingreso": str(aspirante.nivel_ingreso).upper(),
        "fecha": timezone.now().strftime('%d/%m/%Y')
    }
    
    buffer = fill_pdf_form(template_path, data)
    
    if not buffer:
        # Fallback simple si no hay plantilla o hay error
        buffer = io.BytesIO()
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(buffer)
        c.drawString(100, 750, f"CONTRATO - {data['nombre']}")
        c.save()
        buffer.seek(0)
        
    return buffer
