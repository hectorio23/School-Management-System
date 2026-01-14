from rest_framework.permissions import BasePermission

class IsEstudiante(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.is_authenticated and request.user.role in ("estudiante", "Estudiante", "ESTUDIANTE")

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("administrador", "admin", "Admin", "ADMIN", "Administrador")

class IsContador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("accountant", "Accountant", "ACCOUNTANT")

class IsCafeteria(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("cafeteria", "Cafeteria", "CAFETERIA")