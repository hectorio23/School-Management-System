from rest_framework import permissions
from .models import AdministradorEscolar, Maestro

class IsAdministradorEscolar(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'admin_escolar'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin_escolar'

class IsMaestro(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'maestro'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'maestro'

class IsEstudiante(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'estudiante'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'estudiante'

class IsAdminEscolarDelMismoNivel(permissions.BasePermission):
    """
    Verifica que el objeto pertenezca al mismo nivel educativo que el administrador escolar.
    Asume que el objeto tiene un atributo 'nivel_educativo' o una relación a él.
    """
    def has_object_permission(self, request, view, obj):
        if not (request.user.is_authenticated and request.user.role == 'admin_escolar'):
            return False
            
        try:
            admin_perfil = request.user.admin_escolar_perfil
        except AdministradorEscolar.DoesNotExist:
            return False

        # Verificar nivel educativo del objeto
        # Caso 1: El objeto es un NivelEducativo (si aplicara)
        if hasattr(obj, 'nombre') and obj.__class__.__name__ == 'NivelEducativo':
             return obj == admin_perfil.nivel_educativo
             
        # Caso 2: El objeto tiene atributo nivel_educativo directo (Maestro, Admin, Programa)
        if hasattr(obj, 'nivel_educativo'):
            return obj.nivel_educativo == admin_perfil.nivel_educativo
            
        # Caso 3: El objeto tiene relación indirecta (Materia -> Grado -> Nivel ? No, Materia no tiene nivel directo pero Grado si tiene pero es opcional en modelo legacy)
        # Ajuste segun modelos: Materia -> Grado. Grado tiene nivel_educativo? Si, agregamos FK en modelo previo.
        if hasattr(obj, 'grado') and hasattr(obj.grado, 'nivel_educativo'):
             return obj.grado.nivel_educativo == admin_perfil.nivel_educativo

        # Caso 4: Grupo -> Grado -> Nivel
        if hasattr(obj, 'grado') and hasattr(obj.grado, 'nivel_educativo'):
             return obj.grado.nivel_educativo == admin_perfil.nivel_educativo

        # Caso 5: AsignacionMaestro -> Maestro -> Nivel (o Grupo -> Grado -> Nivel)
        if hasattr(obj, 'maestro') and hasattr(obj.maestro, 'nivel_educativo'):
             return obj.maestro.nivel_educativo == admin_perfil.nivel_educativo

        return False

class IsMaestroDelMismoNivel(permissions.BasePermission):
    """
    Verifica que el objeto pertenezca a las asignaciones del maestro.
    """
    def has_object_permission(self, request, view, obj):
        if not (request.user.is_authenticated and request.user.role == 'maestro'):
            return False
            
        try:
            maestro_perfil = request.user.maestro_perfil
        except Maestro.DoesNotExist:
            return False

        # Caso AsignacionMaestro
        if obj.__class__.__name__ == 'AsignacionMaestro':
            return obj.maestro == maestro_perfil
            
        # Caso Calificacion
        if obj.__class__.__name__ == 'Calificacion':
            return obj.asignacion_maestro.maestro == maestro_perfil

        return False
