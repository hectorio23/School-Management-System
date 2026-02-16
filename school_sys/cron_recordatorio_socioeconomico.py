#!/usr/bin/env python
"""
Cronjob: Recordatorio de Estudio Socioeconómico
===============================================

Ejecutar: python manage.py shell < cron_recordatorio_socioeconomico.py
Alternativa: python manage.py runscript cron_recordatorio_socioeconomico (si se usa django-extensions)

Frecuencia recomendada: Mensual (día 1 de cada mes)
Cron: 0 9 1 * *

Comportamiento:
1. Verifica si el ciclo escolar actual termina en los próximos 2 meses
2. Identifica estudiantes sin estudio socioeconómico reciente (> 1 mes)
3. Envía email recordatorio a estudiante y tutores
4. No duplica emails si estudiante y tutor tienen el mismo correo

Variables de entorno:
- MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES: Meses requeridos entre estudios (default: 1)
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
from datetime import timedelta

from estudiantes.models import (
    Estudiante, CicloEscolar, EvaluacionSocioeconomica, 
    EstudianteTutor, EstadoEstudiante, HistorialEstadosEstudiante
)


def enviar_recordatorio_socioeconomico(estudiante, ultimo_estudio):
    """
    Envía recordatorio por email al estudiante y tutores.
    Evita duplicar emails.
    """
    emails_enviados = set()
    
    # Email del estudiante
    email_estudiante = estudiante.usuario.email if estudiante.usuario else None
    
    # Emails de tutores
    tutores = EstudianteTutor.objects.filter(estudiante=estudiante, activo=True)
    emails_tutores = [t.tutor.correo for t in tutores if t.tutor.correo]
    
    # Combinar sin duplicados
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
        return False
    
    # Calcular fecha del último estudio
    fecha_ultimo = "Nunca" if not ultimo_estudio else ultimo_estudio.fecha_evaluacion.strftime("%Y-%m-%d")
    
    subject = f"Recordatorio: Actualización de Estudio Socioeconómico - {estudiante.nombre} {estudiante.apellido_paterno}"
    message = f"""
Estimado padre/madre/tutor,

Le recordamos que es tiempo de actualizar el estudio socioeconómico del estudiante:

Nombre: {estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}
Matrícula: {estudiante.matricula}
Último estudio registrado: {fecha_ultimo}

La actualización del estudio socioeconómico es importante para:
- Mantener actualizado el porcentaje de descuento aplicable
- Garantizar que la beca o apoyo que recibe sea acorde a su situación actual
- Cumplir con los requisitos administrativos del ciclo escolar

Para realizar la actualización, puede:
1. Ingresar al portal de estudiantes y completar el formulario en línea
2. Acudir a la oficina de Trabajo Social en horario de atención

Le agradecemos su pronta atención a este asunto.

Atentamente,
Administración Escolar
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=todos_emails,
            fail_silently=True
        )
        print(f"  [EMAIL] Enviado a: {', '.join(todos_emails)}")
        return True
    except Exception as e:
        print(f"  [ERROR] Email fallido: {str(e)}")
        return False


def enviar_recordatorios_socioeconomico():
    """
    Envía recordatorios de actualización de estudio socioeconómico
    a estudiantes que no han actualizado recientemente.
    """
    print("[CRON] Iniciando envío de recordatorios de estudio socioeconómico...")
    print(f"[INFO] Fecha actual: {timezone.now().date()}")
    
    hoy = timezone.now().date()
    
    # 1. Verificar si el ciclo escolar termina en los próximos 2 meses
    ciclo_activo = CicloEscolar.objects.filter(activo=True).first()
    
    if not ciclo_activo:
        print("[WARN] No hay ciclo escolar activo. Abortando.")
        return
    
    fecha_fin_ciclo = ciclo_activo.fecha_fin
    meses_hasta_fin = (fecha_fin_ciclo.year - hoy.year) * 12 + (fecha_fin_ciclo.month - hoy.month)
    
    print(f"[INFO] Ciclo activo: {ciclo_activo.nombre}")
    print(f"[INFO] Fecha fin de ciclo: {fecha_fin_ciclo}")
    print(f"[INFO] Meses hasta fin de ciclo: {meses_hasta_fin}")
    
    if meses_hasta_fin > 2:
        print("[INFO] El ciclo escolar aún no está próximo a terminar. No se envían recordatorios.")
        return
    
    # 2. Obtener configuración
    MESES_ENTRE_ESTUDIOS = int(os.getenv('MONTHS_BETWEEN_SOCIOECONOMIC_STUDIES', '1'))
    fecha_limite = timezone.now() - timedelta(days=30 * MESES_ENTRE_ESTUDIOS)
    
    print(f"[CONFIG] Meses entre estudios: {MESES_ENTRE_ESTUDIOS}")
    print(f"[CONFIG] Fecha límite para último estudio: {fecha_limite.date()}")
    
    # 3. Obtener estudiantes activos
    estudiantes_activos = Estudiante.objects.filter(
        usuario__activo=True
    )
    
    # Filtrar por estado activo
    estudiantes_activos_verificados = []
    for est in estudiantes_activos:
        estado_actual = est.get_estado_actual()
        if estado_actual and estado_actual.es_estado_activo:
            estudiantes_activos_verificados.append(est)
    
    print(f"[INFO] Estudiantes activos: {len(estudiantes_activos_verificados)}")
    
    # 4. Identificar estudiantes sin estudio reciente
    estudiantes_a_notificar = []
    
    for estudiante in estudiantes_activos_verificados:
        ultimo_estudio = EvaluacionSocioeconomica.objects.filter(
            estudiante=estudiante
        ).order_by('-fecha_evaluacion').first()
        
        if not ultimo_estudio:
            # Nunca ha tenido estudio
            estudiantes_a_notificar.append((estudiante, None))
        elif ultimo_estudio.fecha_evaluacion < fecha_limite:
            # Estudio desactualizado
            estudiantes_a_notificar.append((estudiante, ultimo_estudio))
    
    print(f"[INFO] Estudiantes a notificar: {len(estudiantes_a_notificar)}")
    
    # 5. Enviar notificaciones
    emails_enviados = 0
    errores = 0
    
    for estudiante, ultimo_estudio in estudiantes_a_notificar:
        print(f"\n[PROC] Matrícula: {estudiante.matricula} | {estudiante.nombre} {estudiante.apellido_paterno}")
        
        if enviar_recordatorio_socioeconomico(estudiante, ultimo_estudio):
            emails_enviados += 1
        else:
            errores += 1
    
    print(f"\n[RESULTADO]")
    print(f"  - Total a notificar: {len(estudiantes_a_notificar)}")
    print(f"  - Emails enviados: {emails_enviados}")
    print(f"  - Errores: {errores}")


if __name__ == '__main__':
    enviar_recordatorios_socioeconomico()
else:
    # Si se ejecuta desde manage.py shell
    enviar_recordatorios_socioeconomico()
