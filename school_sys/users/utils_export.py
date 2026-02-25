import io
from django.http import HttpResponse
from django.utils import timezone

# Intentar importar librerías de terceros, manejar error si no existen
try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
except ImportError:
    openpyxl = None
    Font = Alignment = PatternFill = Border = Side = None

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
except ImportError:
    colors = letter = landscape = SimpleDocTemplate = Table = TableStyle = Paragraph = Spacer = getSampleStyleSheet = ParagraphStyle = inch = None

def generar_excel_estudiantes(queryset):
    """Genera un archivo Excel con la lista de estudiantes."""
    if not openpyxl:
        return None

    output = io.BytesIO()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Estudiantes"

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    center_aligned = Alignment(horizontal="center", vertical="center")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # Encabezados
    headers = [
        "Matricula", "Ap. Paterno", "Ap. Materno", "Nombres", "CURP", 
        "Nivel", "Grado", "Grupo", "Estatus", "Beca (%)", "Estrato"
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = thin_border

    # Datos
    for row_num, est in enumerate(queryset, 2):
        grupo_str = "S/A"
        grado_str = "S/A"
        nivel_str = "S/A"
        
        # Resolver relaciones optimizadas
        # Nota: Asumimos que queryset viene con select_related/prefetch_related
        # Pero por seguridad hacemos gets seguros
        
        inscripcion = None
        if hasattr(est, 'active_enrollment') and est.active_enrollment:
             inscripcion = est.active_enrollment[0]
        elif est.inscripciones.filter(grupo__ciclo_escolar__activo=True).exists():
             inscripcion = est.inscripciones.filter(grupo__ciclo_escolar__activo=True).first()
             
        if inscripcion and inscripcion.grupo:
            grupo_str = inscripcion.grupo.nombre
            if inscripcion.grupo.grado:
                grado_str = inscripcion.grupo.grado.nombre
                if inscripcion.grupo.grado.nivel_educativo:
                    nivel_str = inscripcion.grupo.grado.nivel_educativo.nombre
                else:
                    nivel_str = inscripcion.grupo.grado.nivel

        estrato = est.get_estrato_actual()
        estrato_nombre = estrato.nombre if estrato else "Sin Asignar"
        estado = est.get_estado_actual()
        estatus_nombre = estado.nombre if estado else "N/A"

        row = [
            est.matricula,
            est.apellido_paterno,
            est.apellido_materno,
            est.nombre,
            est.usuario.username,
            nivel_str,
            grado_str,
            grupo_str,
            estatus_nombre,
            f"{est.porcentaje_beca}%",
            estrato_nombre
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            cell.border = thin_border
            if col_num in [1, 9, 10]: # Centrar matrícula y status
                cell.alignment = center_aligned

    # Ajustar ancho columnas
    for column_cells in sheet.columns:
        length = max(len(str(cell.value) or "") for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    workbook.save(output)
    output.seek(0)
    return output


def generar_pdf_estudiantes(queryset):
    """Genera un archivo PDF con la lista de estudiantes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    # Título
    elements.append(Paragraph("Reporte General de Estudiantes", title_style))
    elements.append(Paragraph(f"Fecha de emisión: {timezone.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla
    data = [["Matrícula", "Nombre Completo", "Nivel/Grado/Grupo", "Estatus", "Beca"]]
    
    for est in queryset:
        grupo_full = "S/A"
        inscripcion = None
        if hasattr(est, 'active_enrollment') and est.active_enrollment:
             inscripcion = est.active_enrollment[0]
        elif est.inscripciones.filter(grupo__ciclo_escolar__activo=True).exists():
             inscripcion = est.inscripciones.filter(grupo__ciclo_escolar__activo=True).first()

        if inscripcion and inscripcion.grupo:
             g = inscripcion.grupo
             grad = g.grado.nombre if g.grado else "?"
             nivel = g.grado.nivel_educativo.nombre if (g.grado and g.grado.nivel_educativo) else "?"
             grupo_full = f"{nivel} - {grad} {g.nombre}"
        
        estado = est.get_estado_actual()
        estatus = estado.nombre if estado else "N/A"
        
        data.append([
            str(est.matricula),
            f"{est.apellido_paterno} {est.apellido_materno} {est.nombre}",
            grupo_full,
            estatus,
            f"{est.porcentaje_beca}%"
        ])
        
    table = Table(data, colWidths=[1.2*inch, 3.5*inch, 2.5*inch, 1.5*inch, 1*inch])
    
    # Estilo Tabla
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (1,1), (1,-1), 'LEFT'), # Nombre a la izquierda
    ])
    table.setStyle(style)
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer


def generar_excel_aspirantes(queryset):
    """Genera un archivo Excel con la lista de aspirantes."""
    if not openpyxl:
        return None

    output = io.BytesIO()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Aspirantes"

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="E26B0A", end_color="E26B0A", fill_type="solid") # Naranja para diferenciar
    center_aligned = Alignment(horizontal="center", vertical="center")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # Encabezados
    headers = [
        "Folio", "Ap. Paterno", "Ap. Materno", "Nombres", "Email", 
        "Nivel Interés", "Grado Interés", "Estatus Fase", "Pago"
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = thin_border

    # Datos
    for row_num, asp in enumerate(queryset, 2):
        estatus_pago = "Pagado" if asp.pago_inscripcion_realizado else "Pendiente"
        
        row = [
            asp.user.folio,
            asp.apellido_paterno,
            asp.apellido_materno,
            asp.nombre,
            asp.user.email,
            asp.nivel_ingreso,
            asp.grado_ingreso,
            f"Fase {asp.proceso_finalizado_fase}",
            estatus_pago
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            cell.border = thin_border
            if col_num in [1, 8]:
                cell.alignment = center_aligned

    # Ajustar ancho
    for column_cells in sheet.columns:
        length = max(len(str(cell.value) or "") for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    workbook.save(output)
    output.seek(0)
    return output


def generar_pdf_reporte_financiero(data):
    """
    Genera un reporte financiero completo en PDF.
    data: dict con 'resumen', 'por_concepto', 'por_nivel', 'por_estrato', 'becas'.
    """
    if not SimpleDocTemplate:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    h2_style = ParagraphStyle('h2', parent=styles['Heading2'], spaceAfter=10)
    normal_style = styles['Normal']
    
    # 1. Título y Encabezado
    elements.append(Paragraph("Reporte del Estado Financiero Institucional", title_style))
    elements.append(Paragraph(f"Fecha de emisión: {timezone.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))
    
    # 2. Resumen Ejecutivo
    resumen = data.get('resumen', {})
    elements.append(Paragraph("Resumen Ejecutivo", h2_style))
    resumen_data = [
        ["Total Recaudado (Pagos)", f"${resumen.get('total_recaudado', '0.00'):,.2f}"],
        ["Total Deuda Pendiente", f"${resumen.get('total_deuda', '0.00'):,.2f}"],
        ["Alumnos con Beca", f"{resumen.get('becados_pct', '0')}% ({resumen.get('becados_count', '0')} alumnos)"]
    ]
    res_table = Table(resumen_data, colWidths=[3*inch, 2.5*inch])
    res_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(res_table)
    elements.append(Spacer(1, 0.4 * inch))
    
    # 3. Recaudación por Tipo de Concepto
    elements.append(Paragraph("Recaudación por Tipo de Concepto", h2_style))
    conc_data = [["Tipo de Concepto", "Monto Recaudado"]]
    for item in data.get('por_concepto', []):
        conc_data.append([item['tipo'].capitalize(), f"${item['monto']:,.2f}"])
    
    conc_table = Table(conc_data, colWidths=[3.5*inch, 2*inch])
    conc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
    ]))
    elements.append(conc_table)
    elements.append(Spacer(1, 0.4 * inch))
    
    # 4. Deuda por Nivel Educativo
    elements.append(Paragraph("Deuda Pendiente por Nivel Educativo", h2_style))
    lvl_data = [["Nivel Educativo", "Monto de Adeudo"]]
    for item in data.get('por_nivel', []):
        lvl_data.append([item['nivel'], f"${item['monto']:,.2f}"])
    
    lvl_table = Table(lvl_data, colWidths=[3.5*inch, 2*inch])
    lvl_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkred),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
    ]))
    elements.append(lvl_table)
    elements.append(Spacer(1, 0.4 * inch))
    
    # Finalizar
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generar_excel_reporte_financiero(data):
    """Genera un archivo Excel con el reporte financiero."""
    if not openpyxl:
        return None

    output = io.BytesIO()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Reporte Financiero"

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    center_aligned = Alignment(horizontal="center", vertical="center")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # 1. Resumen Ejecutivo
    sheet.append(["Resumen Ejecutivo"])
    sheet.cell(row=1, column=1).font = Font(bold=True, size=14)
    
    resumen = data.get('resumen', {})
    resumen_rows = [
        ["Concepto", "Valor"],
        ["Total Recaudado (Pagos)", resumen.get('total_recaudado', 0)],
        ["Total Deuda Pendiente", resumen.get('total_deuda', 0)],
        ["Alumnos con Beca (%)", resumen.get('becados_pct', 0)],
        ["Alumnos con Beca (Cantidad)", resumen.get('becados_count', 0)]
    ]
    
    start_row = 3
    for i, row in enumerate(resumen_rows):
        for j, val in enumerate(row):
            cell = sheet.cell(row=start_row + i, column=j + 1)
            cell.value = val
            cell.border = thin_border
            if i == 0:
                cell.font = header_font
                cell.fill = header_fill

    # 2. Recaudación por Concepto
    start_row += 7
    sheet.cell(row=start_row, column=1).value = "Recaudación por Tipo de Concepto"
    sheet.cell(row=start_row, column=1).font = Font(bold=True)
    
    header_row = ["Tipo de Concepto", "Monto Recaudado"]
    for j, val in enumerate(header_row):
        cell = sheet.cell(row=start_row + 1, column=j + 1)
        cell.value = val
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        
    for i, item in enumerate(data.get('por_concepto', []), 2):
        sheet.cell(row=start_row + i, column=1).value = item['tipo'].capitalize()
        sheet.cell(row=start_row + i, column=1).border = thin_border
        sheet.cell(row=start_row + i, column=2).value = item['monto']
        sheet.cell(row=start_row + i, column=2).border = thin_border

    # 3. Deuda por Nivel
    start_row += len(data.get('por_concepto', [])) + 3
    sheet.cell(row=start_row, column=1).value = "Deuda Pendiente por Nivel Educativo"
    sheet.cell(row=start_row, column=1).font = Font(bold=True)
    
    header_row = ["Nivel Educativo", "Monto de Adeudo"]
    for j, val in enumerate(header_row):
        cell = sheet.cell(row=start_row + 1, column=j + 1)
        cell.value = val
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        
    for i, item in enumerate(data.get('por_nivel', []), 2):
        sheet.cell(row=start_row + i, column=1).value = item['nivel']
        sheet.cell(row=start_row + i, column=1).border = thin_border
        sheet.cell(row=start_row + i, column=2).value = item['monto']
        sheet.cell(row=start_row + i, column=2).border = thin_border

    # Ajustar ancho
    sheet.column_dimensions['A'].width = 35
    sheet.column_dimensions['B'].width = 20

    workbook.save(output)
    output.seek(0)
    return output
