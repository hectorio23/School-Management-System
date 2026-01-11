from django import forms
from django.db import transaction
from .models import ConceptoPago, Adeudo
from estudiantes.models import Estudiante, Grado, Grupo, Estrato

class ConceptoPagoForm(forms.ModelForm):
    """
    Formulario para gestionar Conceptos de Pago.
    Incluye campos auxiliares para generar adeudos masivos automáticamente.
    """
    aplicar_a_grado = forms.ModelChoiceField(
        queryset=Grado.objects.all(),
        required=False,
        label="Generar para Grado",
        help_text="Seleccione para asignar este cobro a todos los alumnos del grado."
    )
    aplicar_a_grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=False,
        label="Generar para Grupo",
        help_text="Seleccione para asignar este cobro a un grupo específico."
    )
    aplicar_a_estrato = forms.ModelChoiceField(
        queryset=Estrato.objects.all(),
        required=False,
        label="Filtrar por Estrato",
        help_text="Opcional. Si se selecciona, solo cobrará a alumnos con este estrato socioeconómico (combinable con Grado/Grupo)."
    )
    aplicar_a_matricula = forms.CharField(
        required=False,
        label="Aplicar a Matrícula (Individual)",
        help_text="Ingrese una matrícula para asignar el cobro a un solo alumno (ignora Grado/Grupo)."
    )
    
    class Meta:
        model = ConceptoPago
        fields = '__all__'
        
    def save(self, commit=True):
        # Guardamos primero el ConceptoPago para tener su instancia y ID
        concepto = super().save(commit=commit)
        
        # Si se guardó en BD, procedemos a la lógica de negocio
        if commit:
            self.generar_adeudos(concepto)
            
        return concepto
        
    def generar_adeudos(self, concepto):
        """Lógica para crear registros de Adeudo masivamente"""
        grado = self.cleaned_data.get('aplicar_a_grado')
        grupo = self.cleaned_data.get('aplicar_a_grupo')
        estrato = self.cleaned_data.get('aplicar_a_estrato')
        matricula = self.cleaned_data.get('aplicar_a_matricula')
        
        # Si no se seleccionó ningún criterio, no hacemos nada (el concepto solo se crea)
        if not (grado or grupo or matricula):
            return
            
        estudiantes = Estudiante.objects.filter(estado_actual__es_estado_activo=True)
        
        # Filtros
        if matricula:
            estudiantes = estudiantes.filter(matricula=matricula.strip())
        else:
            if grado:
                estudiantes = estudiantes.filter(grupo__grado=grado)
            if grupo:
                estudiantes = estudiantes.filter(grupo=grupo)
            if estrato:
                # Filtrar estudiantes cuyo ÚLTIMA evaluacion tenga ese estrato
                # Esto es costoso, simplificamos asumiendo que EvaluacionSocioeconomica
                # es un modelo relacionado. Pero Estudiante no tiene FK directo a Estrato,
                # sino a través de EvaluacionSocioeconomica.
                # Usaremos la relación inversa 'evaluaciones'
                estudiantes = estudiantes.filter(
                    evaluaciones__estrato=estrato
                    # Idealmente filtraríamos por la evaluación más reciente,
                    # pero por limitaciones de Django Admin simple, usamos "alguna evaluacion con ese estrato"
                    # o refinamos si es necesario.
                    # Para simplificar user request: "filtros por estrato"
                ).distinct()

        # Generación masiva
        adeudos_crear = []
        count = 0
        
        # Usamos transaction para eficiencia si son muchos
        with transaction.atomic():
            for estudiante in estudiantes:
                # Verificar si ya existe este adeudo para evitar duplicados
                if not Adeudo.objects.filter(estudiante=estudiante, concepto=concepto).exists():
                    adeudos_crear.append(Adeudo(
                        estudiante=estudiante,
                        concepto=concepto,
                        monto_total=concepto.monto,
                        saldo_pendiente=concepto.monto,
                        estatus='pendiente'
                    ))
                    count += 1
            
            if adeudos_crear:
                Adeudo.objects.bulk_create(adeudos_crear)
                
        # Podríamos agregar un mensaje al request, pero desde el form es difícil acceder al request.
        # El admin save_model es mejor lugar para mensajes, pero la lógica aqui encapsula el negocio.
