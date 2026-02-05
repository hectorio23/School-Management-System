from django.test import TestCase
from estudiantes.models import NivelEducativo, Grado, Grupo, Inscripcion, Estudiante, CicloEscolar
from estudiantes.services import calcular_siguiente_grado, generar_adeudos_reinscripcion, procesar_reinscripcion_automatica
from pagos.models import Adeudo, ConceptoPago, Pago
from users.models import User
from decimal import Decimal

class AutomationTests(TestCase):
    def setUp(self):
        # 1. Setup Levels, Grades, Cycles
        self.primaria = NivelEducativo.objects.create(nombre="Primaria", orden=2, grados_totales=6)
        self.g1_prim = Grado.objects.create(nombre="1°", nivel="Primaria", nivel_educativo=self.primaria, numero_grado=1, orden_global=4)
        self.g2_prim = Grado.objects.create(nombre="2°", nivel="Primaria", nivel_educativo=self.primaria, numero_grado=2, orden_global=5)
        
        # Ciclo Anterior (que termina)
        self.ciclo_anterior = CicloEscolar.objects.create(nombre="2024-2025", fecha_inicio="2024-08-01", fecha_fin="2025-07-01", activo=True)
        # Ciclo Nuevo (que empieza)
        self.ciclo_nuevo = CicloEscolar.objects.create(nombre="2025-2026", fecha_inicio="2025-08-01", fecha_fin="2026-07-01", activo=False)

        # 2. Setup Groups
        self.grupo_1a = Grupo.objects.create(nombre="A", grado=self.g1_prim, ciclo_escolar=self.ciclo_anterior)
        self.grupo_2a = Grupo.objects.create(nombre="A", grado=self.g2_prim, ciclo_escolar=self.ciclo_nuevo) # Grupo para el siguiente ciclo

        # 3. Setup Student
        self.user = User.objects.create(email="autom@test.com", password="password")
        self.estudiante = Estudiante.objects.create(usuario=self.user, nombre="Auto", apellido_paterno="Test", matricula=2000)
        
        # Inscripción Actual
        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante, 
            grupo=self.grupo_1a, 
            estatus='activo'
        )

        # 4. Setup Concepto Pago Reinscripción (Matching services.py name)
        self.concepto_reinsc, _ = ConceptoPago.objects.get_or_create(
            nombre="Reinscripción Primaria",
            tipo_concepto="reinscripcion",
            nivel_educativo="Primaria",
            defaults={
                'descripcion': "Reinscripción anual",
                'monto_base': 1500.00,
                'activo': True
            }
        )

    def test_generar_adeudo_reinscripcion(self):
        """Test: Generar adeudo al finalizar ciclo"""
        # Ejecutar servicio
        resultados = generar_adeudos_reinscripcion(self.ciclo_anterior)
        
        # Verificar resultados
        self.assertEqual(resultados["procesados"], 1) # fixed typo
        # services.py uses "procesados"
        
    def test_generar_adeudo_integration(self):
        """Integration Test: Full flow debt generation"""
        resultados = generar_adeudos_reinscripcion(self.ciclo_anterior)
        
        self.assertEqual(resultados["procesados"], 1)
        self.assertEqual(resultados["adeudos_creados"], 1, f"Adeudos no creados. Resultados: {resultados}")
        
        # Verificar Adeudo creado
        adeudo = Adeudo.objects.get(
            estudiante=self.estudiante, 
            concepto__nombre="Reinscripción Primaria Automática",
            concepto__nivel_educativo="Primaria"
        )
        self.assertEqual(adeudo.monto_base, Decimal("1500.00"))
        self.assertEqual(adeudo.estatus, 'pendiente')
        
        # Verificar Inscripción estatus actualizado
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estatus, 'pendiente_pago')

    def test_procesar_pago_y_reinscribir(self):
        """Test: Pagar adeudo y reinscribir automáticamente"""
        # 1. Crear Adeudo Manually (como si el job hubiera corrido)
        adeudo = Adeudo.objects.create(
            estudiante=self.estudiante,
            concepto=self.concepto_reinsc,
            monto_base=1500.00,
            estatus='pendiente',
            generado_automaticamente=True
        )
        self.inscripcion.estatus = 'pendiente_pago'
        self.inscripcion.save()
        
        # Activar ciclo nuevo para que funcione la reinscripción
        self.ciclo_anterior.activo = False
        self.ciclo_anterior.save()
        self.ciclo_nuevo.activo = True
        self.ciclo_nuevo.save()
        
        # 2. Simular Pago
        pago = Pago.objects.create(
            adeudo=adeudo,
            monto=1500.00,
            metodo_pago="Transferencia"
        )
        
        # 3. La lógica ya debió ejecutarse vía signal (post_save en Pago)
        # La función procesar_reinscripcion_automatica retornará False en la segunda llamada
        # porque la inscripción ya existe.
        procesar_reinscripcion_automatica(pago)
        
        # 4. Verificar nueva inscripción
        nueva_inscripcion = Inscripcion.objects.get(
            estudiante=self.estudiante,
            grupo__ciclo_escolar=self.ciclo_nuevo
        )
        self.assertEqual(nueva_inscripcion.grupo, self.grupo_2a)
        self.assertEqual(nueva_inscripcion.estatus, 'activo')
        
        # Verificar anterior completada
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estatus, 'completado')
