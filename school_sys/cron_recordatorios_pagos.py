#!/usr/bin/env python
"""
Cronjob: Recordatorios de Pago (RF-NOT-01, RF-NOT-02)
=====================================================

Ejecutar: python manage.py shell < cron_recordatorios_pagos.py

Frecuencia recomendada: Diaria (ej. 08:00 AM)
Cron: 0 8 * * *

Lógica:
1.  RF-NOT-01: Buscar adeudos que vencen en 5 días.
2.  RF-NOT-02: Buscar adeudos que vencen mañana (1 día).
3.  Enviar correo a estudiante y tutores.
"""

import os
import django
from datetime import timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from pagos.models import Adeudo
from estudiantes.models import EstudianteTutor

def enviar_aviso_pago(adeudo, dias_para_vencer):
    """Envía el correo de recordatorio"""
    estudiante = adeudo.estudiante
    concepto = adeudo.concepto.nombre
    monto = adeudo.monto_total
    fecha_vencimiento = adeudo.fecha_vencimiento
    
    # Destinatarios
    emails = set()
    if estudiante.usuario.email:
        emails.add(estudiante.usuario.email)
        
    tutores = EstudianteTutor.objects.filter(estudiante=estudiante, activo=True)
    for t in tutores:
        if t.tutor.correo:
            emails.add(t.tutor.correo)
            
    if not emails:
        print(f"  [WARN] Sin emails para notificar - Matrícula {estudiante.matricula}")
        return False
        
    subject = f"Recordatorio de Pago: {concepto} vence en {dias_para_vencer} días"
    if dias_para_vencer == 1:
        subject = f"URGENTE: Su pago de {concepto} vence MAÑANA"
        
    mensaje = f"""
    Estimado estudiante/padre de familia:
    
    Le recordamos que el pago correspondiente al concepto:
    
    Concepto: {concepto}
    Monto a pagar: ${monto}
    Fecha límite: {fecha_vencimiento}
    
    {"Evite recargos realizando su pago a tiempo." if dias_para_vencer > 1 else "ATENCIÓN: Si no realiza el pago mañana, se aplicarán recargos automáticos (10% + $125.00 MXN)."}
    
    Puede realizar su pago en ventanilla o subir su comprobante a través del portal.
    
    Atentamente,
    Administración Escolar
    """
    
    try:
        send_mail(
            subject=subject,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(emails),
            fail_silently=True
        )
        print(f"  [EMAIL] Enviado a {', '.join(emails)} - Adeudo {adeudo.id}")
        return True
    except Exception as e:
        print(f"  [ERROR] Falló envío para adeudo {adeudo.id}: {e}")
        return False

def ejecutar_notificaciones():
    print(f"[CRON] Iniciando recordatorios de pago - {timezone.now()}")
    
    hoy = timezone.now().date()
    
    # 1. RF-NOT-01: 5 Días antes
    target_date_5 = hoy + timedelta(days=5)
    adeudos_5 = Adeudo.objects.filter(
        fecha_vencimiento=target_date_5,
        estatus__in=['pendiente', 'parcial']
    ).select_related('estudiante', 'estudiante__usuario', 'concepto')
    
    print(f"[INFO] Adeudos que vencen en 5 días ({target_date_5}): {adeudos_5.count()}")
    for adeudo in adeudos_5:
        enviar_aviso_pago(adeudo, 5)
        
    # 2. RF-NOT-02: 1 Día antes (Mañana)
    target_date_1 = hoy + timedelta(days=1)
    adeudos_1 = Adeudo.objects.filter(
        fecha_vencimiento=target_date_1,
        estatus__in=['pendiente', 'parcial']
    ).select_related('estudiante', 'estudiante__usuario', 'concepto')
    
    print(f"[INFO] Adeudos que vencen MAÑANA ({target_date_1}): {adeudos_1.count()}")
    for adeudo in adeudos_1:
        enviar_aviso_pago(adeudo, 1)
        
    print("[CRON] Finalizado.")

if __name__ == '__main__':
    ejecutar_notificaciones()
