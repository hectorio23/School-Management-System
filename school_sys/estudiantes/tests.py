from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Estudiante, Estrato, EvaluacionSocioeconomica
from django.core.files.uploadedfile import SimpleUploadedFile

class EstudioSocioeconomicoTests(APITestCase):
    def setUp(self):
        # Crear usuario y estudiante
        self.user = User.objects.create_user(
            email='test@example.com', 
            password='testpassword',
            role='estudiante'
        )
        self.estudiante = Estudiante.objects.create(
            usuario=self.user,
            matricula=123456,
            nombre="Juan",
            apellido_paterno="Perez",
            apellido_materno="Lopez",
            direccion="Calle Falsa 123"
        )
        
        # Crear estratos
        self.estrato_a = Estrato.objects.create(nombre='A', porcentaje_descuento=10.00)
        self.estrato_b = Estrato.objects.create(nombre='B', porcentaje_descuento=20.00)
        
        # Autenticar
        self.client.force_authenticate(user=self.user)
        self.url = reverse('estudio_socioeconomico')

    def test_create_estudio_stratum_b(self):
        """Test que verifica asignación de Estrato B para ingreso <= 10000"""
        data = {
            "ingreso_mensual": 8000.00,
            "tipo_vivienda": "Propia",
            "miembros_hogar": 4
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EvaluacionSocioeconomica.objects.count(), 1)
        
        evaluacion = EvaluacionSocioeconomica.objects.first()
        self.assertEqual(evaluacion.estrato, self.estrato_b)
        self.assertEqual(response.data['estrato_asignado'], 'B')

    def test_create_estudio_stratum_a(self):
        """Test que verifica asignación de Estrato A para ingreso > 10000"""
        data = {
            "ingreso_mensual": 15000.00,
            "tipo_vivienda": "Rentada",
            "miembros_hogar": 2
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        evaluacion = EvaluacionSocioeconomica.objects.first()
        self.assertEqual(evaluacion.estrato, self.estrato_a)
        self.assertEqual(response.data['estrato_asignado'], 'A')
        
    def test_create_estudio_with_files(self):
        """Test de subida de archivos (Acta y CURP)"""
        acta = SimpleUploadedFile("acta.pdf", b"file_content", content_type="application/pdf")
        curp = SimpleUploadedFile("curp.pdf", b"file_content", content_type="application/pdf")
        
        data = {
            "ingreso_mensual": 5000.00,
            "tipo_vivienda": "Familiar",
            "miembros_hogar": 5,
            "acta_nacimiento": acta,
            "curp": curp
        }
        # MultiPart is handled automatically by client.post when files are present usually, 
        # but explicit check is good.
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify stub function didn't crash
        
    def test_missing_fields(self):
        """Test validación de campos requeridos"""
        data = {
            "ingreso_mensual": 5000.00
            # Missing tipo_vivienda and miembros_hogar
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
