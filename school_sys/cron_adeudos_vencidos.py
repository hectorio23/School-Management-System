#!/usr/bin/env python
"""
Cronjob: Recálculo de adeudos vencidos y Multas de Biblioteca
============================================================

Ejecutar: python manage.py shell < cron_adeudos_vencidos.py
Alternativa: python manage.py runscript cron_adeudos_vencidos (si se usa django-extensions)

Frecuencia recomendada: Diario a las 00:01 AM
Cron: 1 0 * * *

Comportamiento:
1. Detecta adeudos vencidos (fecha_vencimiento < hoy)
2. Aplica recargos financieros
3. Detecta préstamos de biblioteca vencidos
4. Genera multas y envía notificaciones
"""

import os
import sys
import django

# Configurar Django si no está configurado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from datetime import timedelta

from estudiantes.models import Estudiante, EstadoEstudiante, HistorialEstadosEstudiante, EstudianteTutor
from pagos.models import Adeudo
from biblioteca.models import Prestamo, Multa


def enviar_notificacion_adeudo(estudiante, adeudo, es_baja=False):
    """
    Envía notificación por email al estudiante y tutores por adeudos financieros.
    """
    emails_enviados = set()
    email_estudiante = estudiante.usuario.email if estudiante.usuario else None
    
    tutores = EstudianteTutor.objects.filter(estudiante=estudiante, activo=True)
    emails_tutores = [t.tutor.correo for t in tutores if t.tutor.correo]
    
    todos_emails = []
    if email_estudiante and email_estudiante not in emails_enviados:
        todos_emails.append(email_estudiante)
        emails_enviados.add(email_estudiante)
    
    for email in emails_tutores:
        if email and email not in emails_enviados:
            todos_emails.append(email)
            emails_enviados.add(email)
    
    if not todos_emails:
        print(f"  [WARN] Sin emails para notificar - Matrícula {estudiante.matricula}")
        return
    
    if es_baja:
        subject = f"[URGENTE] Baja por Falta de Pago - {estudiante.nombre} {estudiante.apellido_paterno or estudiante.apellido_materno}"
        message = f"Estimado padre/madre/tutor,\n\nEl estudiante {estudiante.nombre} {estudiante.apellido_paterno} ha sido dado de baja por falta de pago.\n\nMonto total: ${adeudo.monto_total}\n\nAtentamente,\nAdministración Escolar"
    else:
        subject = f"Aviso de Adeudo Vencido - {estudiante.nombre} {estudiante.apellido_paterno}"
        message = f"Estimado padre/madre/tutor,\n\nEl estudiante {estudiante.nombre} {estudiante.apellido_paterno} tiene un adeudo vencido.\n\nMonto total: ${adeudo.monto_total}\n\nAtentamente,\nAdministración Escolar"
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=todos_emails,
            fail_silently=True
        )
        print(f"  [EMAIL] Enviado a: {', '.join(todos_emails)}")
    except Exception as e:
        print(f"  [ERROR] Email fallido: {str(e)}")


def enviar_notificacion_multa_biblioteca(estudiante_user, multa):
    """
    Envía notificación de multa de biblioteca al estudiante.
    """
    if not estudiante_user.email:
        print(f"  [WARN] Sin email para notificar multa - Usuario {estudiante_user.id}")
        return
        
    subject = f"Multa de Biblioteca Pendiente - {multa.prestamo.libro.titulo}"
    message = f"""
Hola {multa.prestamo.usuario.nombre},

Te informamos que el préstamo del libro "{multa.prestamo.libro.titulo}" ha vencido
con fecha {multa.prestamo.fecha_de_devolucion}.

Se ha generado una multa por la cantidad de ${multa.monto}.

Por favor, acude a la biblioteca para devolver el libro y realizar el pago correspondiente.

Atentamente,
Departamento de Biblioteca
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[estudiante_user.email],
            fail_silently=True
        )
        print(f"  [EMAIL] Notificación de multa enviada a: {estudiante_user.email}")
    except Exception as e:
        print(f"  [ERROR] Email de multa fallido: {str(e)}")


def procesar_adeudos_vencidos():
    """
    Procesa todos los adeudos vencidos aplicando recargos
    y dando de baja estudiantes según las reglas definidas.
    """
    print("[CRON] Iniciando procesamiento de adeudos vencidos...")
    hoy = timezone.now().date()
    
    RECARGO_FIJO = Decimal(os.getenv('OVERDUE_FIXED_SURCHARGE', '125'))
    PORCENTAJE_DIARIO = Decimal(os.getenv('OVERDUE_DAILY_PERCENTAGE', '10')) / 100
    DIAS_BAJA = int(os.getenv('DAYS_BEFORE_DEACTIVATION', '10'))
    
    adeudos_vencidos = Adeudo.objects.filter(
        fecha_vencimiento__lt=hoy,
        estatus__in=['pendiente', 'parcial', 'vencido'],
        adeudo_congelado=False
    )
    
    estado_baja, _ = EstadoEstudiante.objects.get_or_create(
        nombre='Baja por Falta de Pago',
        defaults={'es_estado_activo': False}
    )
    
    with transaction.atomic():
        for adeudo in adeudos_vencidos:
            try:
                dias_mora = (hoy - adeudo.fecha_vencimiento).days
                adeudo.dias_mora = dias_mora
                estudiante = adeudo.estudiante
                
                if dias_mora >= DIAS_BAJA:
                    adeudo.adeudo_congelado = True
                    adeudo.estatus = 'vencido'
                    adeudo.save()
                    HistorialEstadosEstudiante.objects.create(
                        estudiante=estudiante, estado=estado_baja,
                        justificacion=f'Baja automática por adeudo de {dias_mora} días',
                        fecha_baja=hoy
                    )
                    if estudiante.usuario:
                        estudiante.usuario.activo = False
                        estudiante.usuario.save()
                    enviar_notificacion_adeudo(estudiante, adeudo, es_baja=True)
                else:
                    monto_neto = adeudo.monto_base - adeudo.descuento_aplicado
                    recargo_nuevo = Decimal('0.00')
                    if not adeudo.recargo_fijo_aplicado:
                        recargo_nuevo += RECARGO_FIJO
                        adeudo.recargo_fijo_aplicado = True
                    if dias_mora > 1:
                        recargo_diario = monto_neto * PORCENTAJE_DIARIO
                        recargo_nuevo += recargo_diario
                    adeudo.recargo_aplicado += recargo_nuevo
                    adeudo.monto_total = monto_neto + adeudo.recargo_aplicado
                    adeudo.estatus = 'vencido'
                    adeudo.save()
                    if dias_mora == 1 or dias_mora % 3 == 0:
                        enviar_notificacion_adeudo(estudiante, adeudo, es_baja=False)
            except Exception as e:
                print(f"  [ERROR] Adeudo {adeudo.id}: {str(e)}")


def procesar_multas_biblioteca():
    """
    Busca préstamos vencidos y genera multas si no existen.
    """
    print("\n[CRON] Iniciando procesamiento de multas de biblioteca...")
    hoy = timezone.now().date()
    
    prestamos_vencidos = Prestamo.objects.filter(
        fecha_de_devolucion__lt=hoy,
        estado='activo'
    )
    
    MONTO_MULTA = Decimal('50.00') # Monto fijo por retraso según requerimiento implícito
    
    for prestamo in prestamos_vencidos:
        with transaction.atomic():
            prestamo.estado = 'vencido'
            prestamo.save()
            
            multa, created = Multa.objects.get_or_create(
                prestamo=prestamo,
                defaults={'monto': MONTO_MULTA, 'estado': 'pendiente'}
            )
            
            if created:
                print(f"  [MULTA] Nueva para {prestamo.usuario.nombre} - Libro: {prestamo.libro.titulo}")
                enviar_notificacion_multa_biblioteca(prestamo.usuario.usuario, multa)


def procesar_todo():
    procesar_adeudos_vencidos()
    procesar_multas_biblioteca()


if __name__ == '__main__':
    procesar_todo()
else:
    procesar_todo()
