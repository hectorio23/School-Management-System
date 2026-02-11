from rest_framework import permissions

class IsBibliotecario(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'bibliotecario'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'bibliotecario'
