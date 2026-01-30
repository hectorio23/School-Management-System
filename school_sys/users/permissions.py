from rest_framework.permissions import BasePermission

# =============================================================================
# PERMISOS BASADOS EN ROL (USUARIOS)
# =============================================================================

class IsEstudiante(BasePermission):
    """Permite acceso únicamente a usuarios con rol de estudiante."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "estudiante"

class IsAdministrador(BasePermission):
    """Permite acceso a cualquier tipo de administrador (rol base)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "administrador"

class IsContador(BasePermission):
    """Permite acceso únicamente a usuarios con rol de contador."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "contador"

class IsCafeteria(BasePermission):
    """Permite acceso únicamente a usuarios con rol de cafetería."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "cafeteria"


# =============================================================================
# PERMISOS BASADOS EN GRUPOS DE DJANGO (ADMINISTRADORES GRANULARES)
# Estos grupos se asignan desde el panel de administración de Django.
# Un superusuario siempre tiene acceso completo.
# =============================================================================

class HasGroupPermission(BasePermission):
    """
    Clase base para verificar pertenencia a un grupo de Django.
    Los grupos disponibles son:
      - gestor_becas: Gestión de becas y asignaciones
      - gestor_comedor: Gestión del comedor y asistencias
      - gestor_admisiones: Gestión del proceso de admisión
      - admin_ti: Administrador general con todos los permisos
    """
    required_group = None
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Los superusuarios siempre tienen acceso
        if request.user.is_superuser:
            return True
        # Administrador TI tiene acceso a todo
        if request.user.groups.filter(name="admin_ti").exists():
            return True
        # Verificar grupo específico
        if self.required_group:
            return request.user.groups.filter(name=self.required_group).exists()
        return False


class IsGestorBecas(HasGroupPermission):
    """Permite acceso a gestores de becas o admin TI."""
    required_group = "gestor_becas"


class IsGestorComedor(HasGroupPermission):
    """Permite acceso a gestores del comedor o admin TI."""
    required_group = "gestor_comedor"


class IsGestorAdmisiones(HasGroupPermission):
    """Permite acceso a gestores de admisiones o admin TI."""
    required_group = "gestor_admisiones"


class IsAdminTI(HasGroupPermission):
    """Permite acceso únicamente a administradores de TI (acceso total)."""
    required_group = "admin_ti"


# =============================================================================
# PERMISOS COMBINADOS (OR)
# =============================================================================

class IsAdminOrGestorBecas(BasePermission):
    """Combina: Administrador base O Gestor de Becas O Admin TI."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.role == "administrador":
            return True
        return request.user.groups.filter(name__in=["gestor_becas", "admin_ti"]).exists()


class IsAdminOrGestorComedor(BasePermission):
    """Combina: Administrador base O Gestor de Comedor O Admin TI."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.role in ["administrador", "cafeteria"]:
            return True
        return request.user.groups.filter(name__in=["gestor_comedor", "admin_ti"]).exists()


class IsAdminOrGestorAdmisiones(BasePermission):
    """Combina: Administrador base O Gestor de Admisiones O Admin TI."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.role == "administrador":
            return True
        return request.user.groups.filter(name__in=["gestor_admisiones", "admin_ti"]).exists()