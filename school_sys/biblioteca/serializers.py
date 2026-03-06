from rest_framework import serializers
from .models import Libro, UsuarioBiblioteca, Prestamo, Multa
from users.models import User

class LibroSerializer(serializers.ModelSerializer):
    disponibles = serializers.IntegerField(source='ejemplares_disponibles', read_only=True)

    class Meta:
        model = Libro
        fields = '__all__'

class UsuarioBibliotecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioBiblioteca
        fields = '__all__'

class PrestamoSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    
    class Meta:
        model = Prestamo
        fields = '__all__'

class MultaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='prestamo.usuario.nombre', read_only=True)
    libro_titulo = serializers.CharField(source='prestamo.libro.titulo', read_only=True)

    class Meta:
        model = Multa
        fields = '__all__'
