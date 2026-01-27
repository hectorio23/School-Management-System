from rest_framework.permissions import BasePermission
from .models import AdmissionUser

class IsAspirante(BasePermission):
    """
    Clase que permite que únicamente los Aspirantes puedan acceder a el modulo de inscipciones.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            isinstance(request.user, AdmissionUser) and 
            request.user.is_active
        )