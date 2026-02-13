#!/usr/bin/env python
"""
Cronjob: Limpieza de Usuarios Huérfanos
========================================

Ejecutar: python manage.py shell < cron_usuarios_huerfanos.py

Frecuencia recomendada: Diaria (03:00 AM)
Cron: 0 3 * * *

Lógica:
1.  Buscar usuarios con rol 'estudiante' sin perfil en tabla Estudiante.
2.  Buscar usuarios con rol 'maestro' sin perfil en tabla Maestro.
3.  Buscar usuarios sin rol asignado (rol vacío o nulo).
4.  Excluir usuarios con roles administrativos.
5.  Eliminar usuarios huérfanos encontrados.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_sys.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q
from users.models import User

# Roles administrativos que no requieren perfil de estudiante o maestro
ROLES_ADMIN = [
    'administrador', 'becas_admin', 'finanzas_admin',
    'comedor_admin', 'admisiones_admin', 'admin_escolar', 'bibliotecario'
]


def limpiar_usuarios_huerfanos():
    """Elimina usuarios que no tienen un perfil asociado según su rol."""
    print(f"[CRON] Iniciando limpieza de usuarios huérfanos - {timezone.now()}")

    total_eliminados = 0
    errores = 0

    # 1. Estudiantes sin perfil
    estudiantes_huerfanos = User.objects.filter(
        role='estudiante'
    ).exclude(
        perfil_estudiante__isnull=False
    )

    print(f"[INFO] Usuarios con rol 'estudiante' sin perfil: {estudiantes_huerfanos.count()}")

    for usuario in estudiantes_huerfanos:
        try:
            print(f"  [DEL] Usuario huérfano (estudiante): {usuario.email} (ID: {usuario.id})")
            usuario.delete()
            total_eliminados += 1
        except Exception as e:
            print(f"  [ERROR] No se pudo eliminar {usuario.email}: {e}")
            errores += 1

    # 2. Maestros sin perfil
    maestros_huerfanos = User.objects.filter(
        role='maestro'
    ).exclude(
        maestro_perfil__isnull=False
    )

    print(f"[INFO] Usuarios con rol 'maestro' sin perfil: {maestros_huerfanos.count()}")

    for usuario in maestros_huerfanos:
        try:
            print(f"  [DEL] Usuario huérfano (maestro): {usuario.email} (ID: {usuario.id})")
            usuario.delete()
            total_eliminados += 1
        except Exception as e:
            print(f"  [ERROR] No se pudo eliminar {usuario.email}: {e}")
            errores += 1

    # 3. Usuarios sin rol válido (excluyendo administradores)
    usuarios_sin_rol = User.objects.filter(
        Q(role__isnull=True) | Q(role='')
    ).exclude(
        role__in=ROLES_ADMIN
    ).exclude(
        is_superuser=True
    )

    print(f"[INFO] Usuarios sin rol asignado: {usuarios_sin_rol.count()}")

    for usuario in usuarios_sin_rol:
        try:
            print(f"  [DEL] Usuario sin rol: {usuario.email} (ID: {usuario.id})")
            usuario.delete()
            total_eliminados += 1
        except Exception as e:
            print(f"  [ERROR] No se pudo eliminar {usuario.email}: {e}")
            errores += 1

    print(f"\n[RESULTADO]")
    print(f"  - Total eliminados: {total_eliminados}")
    print(f"  - Errores: {errores}")
    print(f"[CRON] Finalizado.")


if __name__ == '__main__':
    limpiar_usuarios_huerfanos()
else:
    # Si se ejecuta desde manage.py shell
    limpiar_usuarios_huerfanos()
