from django.core.management.base import BaseCommand
from estudiantes.services import generar_adeudos_reinscripcion
from estudiantes.models import CicloEscolar
from django.utils import timezone

class Command(BaseCommand):
    help = 'Genera adeudos de reinscripción para alumnos activos del ciclo actual'

    def handle(self, *args, **kwargs):
        # 1. Obtener ciclo activo
        ciclo_actual = CicloEscolar.objects.filter(activo=True).first()
        
        if not ciclo_actual:
            self.stdout.write(self.style.ERROR('No hay un ciclo escolar activo actualmente.'))
            return

        self.stdout.write(f'Generando adeudos para ciclo que termina: {ciclo_actual}')
        
        # Ejecutar servicio
        resultados = generar_adeudos_reinscripcion(ciclo_actual)
        
        if "error" in resultados:
            self.stdout.write(self.style.ERROR(f'Error: {resultados["error"]}'))
            return
            
        self.stdout.write(self.style.SUCCESS('Proceso completado.'))
        self.stdout.write(f'- Procesados: {resultados["procesados"]}')
        self.stdout.write(f'- Egresados: {resultados["egresados"]}')
        self.stdout.write(f'- Adeudos creados: {resultados["adeudos_creados"]}')
        
        if resultados["errores"]:
            self.stdout.write(self.style.WARNING('Errores encontrados:'))
            for error in resultados["errores"]:
                self.stdout.write(f'- {error}')
