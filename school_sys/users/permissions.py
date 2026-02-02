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
# PERMISOS COMBINADOS (OR) - BASADOS EN ROLES ESPECIALIZADOS
# Estos permisos utilizan el campo 'role' del modelo User.
# El rol 'administrador' (TI) siempre tiene acceso completo.
# =============================================================================

class CanAccessStudentInfo(BasePermission):
    """
    Permite acceso a información de estudiantes (listar/detalle).
    Roles permitidos: administrador, becas_admin, finanzas_admin, comedor_admin
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        allowed_roles = ['administrador', 'becas_admin', 'finanzas_admin', 'comedor_admin']
        return request.user.role in allowed_roles


class CanManageBecas(BasePermission):
    """
    CRUD completo de becas, estratos, asignaciones y evaluaciones socioeconómicas.
    Roles permitidos: administrador, becas_admin
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in ['administrador', 'becas_admin']


class CanManageFinanzas(BasePermission):
    """
    CRUD de adeudos, pagos, conceptos y reportes financieros.
    Roles permitidos: administrador, finanzas_admin
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in ['administrador', 'finanzas_admin']


class CanManageComedor(BasePermission):
    """
    Gestión del comedor: asistencias, menús y reportes.
    Roles permitidos: administrador, comedor_admin
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in ['administrador', 'comedor_admin']


class CanManageAdmisiones(BasePermission):
    """
    Gestión del módulo de admisiones: aspirantes, migraciones, documentos.
    Roles permitidos: administrador, admisiones_admin
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in ['administrador', 'admisiones_admin']


# =============================================================================
# PERMISOS COMBINADOS LEGACY (OR) - COMPATIBILIDAD CON GRUPOS DE DJANGO
# Mantener por compatibilidad con el sistema existente.
# =============================================================================

class IsAdminOrGestorBecas(BasePermission):
    """Combina: Administrador TI O becas_admin O Gestor de Becas (grupo)."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.role in ['administrador', 'becas_admin']:
            return True
        return request.user.groups.filter(name__in=["gestor_becas", "admin_ti"]).exists()


class IsAdminOrGestorComedor(BasePermission):
    """Combina: Administrador TI O comedor_admin O Gestor de Comedor (grupo)."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.role in ['administrador', 'comedor_admin', 'cafeteria']:
            return True
        return request.user.groups.filter(name__in=["gestor_comedor", "admin_ti"]).exists()


class IsAdminOrGestorAdmisiones(BasePermission):
    """Combina: Administrador TI O admisiones_admin O Gestor de Admisiones (grupo)."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.role in ['administrador', 'admisiones_admin']:
            return True
        return request.user.groups.filter(name__in=["gestor_admisiones", "admin_ti"]).exists()