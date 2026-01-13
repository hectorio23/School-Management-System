from rest_framework.permissions import BasePermission

class IsEstudiante(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "estudiante"

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "administrador"

class IsContador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "contador"

class IsCafeteria(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "cafeteria"