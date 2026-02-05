from django.test import TestCase
from estudiantes.models import NivelEducativo, Grado, Grupo, Inscripcion, Estudiante, CicloEscolar
from estudiantes.services import calcular_siguiente_grado
from users.models import User

class PromotionLogicTests(TestCase):
    def setUp(self):
        # Setup Levels
        self.preescolar = NivelEducativo.objects.create(nombre="Preescolar", orden=1, grados_totales=3)
        self.primaria = NivelEducativo.objects.create(nombre="Primaria", orden=2, grados_totales=6)
        self.secundaria = NivelEducativo.objects.create(nombre="Secundaria", orden=3, grados_totales=3)

        # Setup Grades
        self.g1_preescolar = Grado.objects.create(nombre="1°", nivel="Preescolar", nivel_educativo=self.preescolar, numero_grado=1, orden_global=1)
        self.g2_preescolar = Grado.objects.create(nombre="2°", nivel="Preescolar", nivel_educativo=self.preescolar, numero_grado=2, orden_global=2)
        self.g3_preescolar = Grado.objects.create(nombre="3°", nivel="Preescolar", nivel_educativo=self.preescolar, numero_grado=3, orden_global=3)
        
        self.g1_primaria = Grado.objects.create(nombre="1°", nivel="Primaria", nivel_educativo=self.primaria, numero_grado=1, orden_global=4)
        self.g6_primaria = Grado.objects.create(nombre="6°", nivel="Primaria", nivel_educativo=self.primaria, numero_grado=6, orden_global=9)
        
        self.g1_secundaria = Grado.objects.create(nombre="1°", nivel="Secundaria", nivel_educativo=self.secundaria, numero_grado=1, orden_global=10)
        self.g3_secundaria = Grado.objects.create(nombre="3°", nivel="Secundaria", nivel_educativo=self.secundaria, numero_grado=3, orden_global=12)

        # Setup Cycle
        self.ciclo = CicloEscolar.objects.create(nombre="2024-2025", fecha_inicio="2024-08-01", fecha_fin="2025-07-01", activo=True)

        # Setup Groups
        self.grupo_prees_1 = Grupo.objects.create(nombre="A", grado=self.g1_preescolar, ciclo_escolar=self.ciclo)
        self.grupo_prees_3 = Grupo.objects.create(nombre="A", grado=self.g3_preescolar, ciclo_escolar=self.ciclo)
        self.grupo_prim_1 = Grupo.objects.create(nombre="A", grado=self.g1_primaria, ciclo_escolar=self.ciclo)
        self.grupo_prim_6 = Grupo.objects.create(nombre="A", grado=self.g6_primaria, ciclo_escolar=self.ciclo)
        self.grupo_sec_3 = Grupo.objects.create(nombre="A", grado=self.g3_secundaria, ciclo_escolar=self.ciclo)

        # Setup User/Student (mock)
        self.user = User.objects.create(email="test@test.com", password="password")
        self.estudiante = Estudiante.objects.create(usuario=self.user, nombre="Test", apellido_paterno="User", matricula=1000)

    def test_promotion_within_level(self):
        """Test: 1° Preescolar -> 2° Preescolar"""
        inscripcion = Inscripcion.objects.create(estudiante=self.estudiante, grupo=self.grupo_prees_1)
        
        siguiente = calcular_siguiente_grado(inscripcion)
        self.assertEqual(siguiente, self.g2_preescolar)

    def test_promotion_change_level_prees_to_prim(self):
        """Test: 3° Preescolar -> 1° Primaria"""
        inscripcion = Inscripcion.objects.create(estudiante=self.estudiante, grupo=self.grupo_prees_3)
        
        siguiente = calcular_siguiente_grado(inscripcion)
        self.assertEqual(siguiente, self.g1_primaria)

    def test_promotion_change_level_prim_to_sec(self):
        """Test: 6° Primaria -> 1° Secundaria"""
        inscripcion = Inscripcion.objects.create(estudiante=self.estudiante, grupo=self.grupo_prim_6)
        
        siguiente = calcular_siguiente_grado(inscripcion)
        # We didn't explicitly create G1 Secundaria but logic should find it if it exists. 
        # Wait, I did in setUp.
        self.assertEqual(siguiente, self.g1_secundaria)

    def test_promotion_graduation(self):
        """Test: 3° Secundaria -> EGRESADO"""
        inscripcion = Inscripcion.objects.create(estudiante=self.estudiante, grupo=self.grupo_sec_3)
        
        siguiente = calcular_siguiente_grado(inscripcion)
        self.assertEqual(siguiente, "EGRESADO")
