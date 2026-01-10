from estudiantes.serializer import SerializerStudent
from rest_framework import viewsets
from estudiantes.models import Estudiante
from django.shortcuts import render

def index(request):
    return render(request, "index.html")
    pass

class StudentViewSet(viewsets.ModelViewSet):
    """
    Endpoints para estudiantes
    GET /api/students/ - Solo admins pueden listar todos
    GET /api/students/{id}/ - Owner o admin
    PUT/PATCH /api/students/{id}/ - Owner o admin
    DELETE /api/students/{id}/ - Solo admin
    """
    queryset = Estudiante.objects.all()
    serializer_class = SerializerStudent
    
    def get_permissions(self):
        if self.action == 'list':
            # Solo admins listan todos
            permission_classes = [IsAuthenticatedWithValidToken, IsAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Owner o admin
            permission_classes = [IsAuthenticatedWithValidToken, IsOwnerOrAdmin]
        elif self.action == 'destroy':
            # Solo admin
            permission_classes = [IsAuthenticatedWithValidToken, IsAdmin]
        else:
            permission_classes = [IsAuthenticatedWithValidToken]
        
        return [permission() for permission in permission_classes]