from django import forms
from django.db import transaction
from decimal import Decimal
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
    aplicar_a_nivel = forms.ChoiceField(
        choices=[], # Se llena en __init__
        required=False,
        label="Generar por Escolaridad (Nivel)",
        help_text="Seleccione para asignar este cobro a todos los alumnos de un nivel educativo."
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar niveles dinámicamente desde los grados existentes
        niveles = NivelEducativo.objects.all().order_by('orden')
        choices = [('', '-- Seleccionar --')] + [(n.nombre, n.nombre) for n in niveles]
        self.fields['aplicar_a_nivel'].choices = choices
    
    class Meta:
        model = ConceptoPago
        fields = '__all__'
        
    def generar_adeudos(self, concepto):
        """
        Lógica para crear registros de Adeudo masivamente.
        """
        grado = self.cleaned_data.get('aplicar_a_grado')
        grupo = self.cleaned_data.get('aplicar_a_grupo')
        nivel = self.cleaned_data.get('aplicar_a_nivel')
        estrato = self.cleaned_data.get('aplicar_a_estrato')
        matricula = self.cleaned_data.get('aplicar_a_matricula')
        
        # Si no se seleccionó ningún criterio, terminamos
        if not (grado or grupo or matricula or nivel or estrato):
            return
            
        # Obtener query inicial
        estudiantes = Estudiante.objects.all()
        
        # Aplicar filtros (AND lógico)
        if matricula:
            estudiantes = estudiantes.filter(matricula=matricula.strip())
        else:
            if nivel:
                estudiantes = estudiantes.filter(inscripciones__grupo__grado__nivel_educativo__nombre=nivel, inscripciones__grupo__ciclo_escolar__activo=True)
            if grado:
                estudiantes = estudiantes.filter(inscripciones__grupo__grado=grado, inscripciones__grupo__ciclo_escolar__activo=True)
            if grupo:
                estudiantes = estudiantes.filter(inscripciones__grupo=grupo, inscripciones__grupo__ciclo_escolar__activo=True)
            estudiantes = estudiantes.distinct()
        
        count = 0
        with transaction.atomic():
            for estudiante in estudiantes:
                # Verificar estado activo
                estado = estudiante.get_estado_actual()
                
                if not estado or not estado.es_estado_activo:
                    continue

                if estrato:
                    estrato_actual = estudiante.get_estrato_actual()
                    if estrato_actual != estrato:
                        continue

                # Verificar duplicados
                existe = Adeudo.objects.filter(estudiante=estudiante, concepto=concepto).exists()
                if not existe:
                    adeudo = Adeudo(
                        estudiante=estudiante,
                        concepto=concepto,
                        monto_base=concepto.monto_base,
                        estatus='pendiente'
                    )
                    adeudo.save()
                    count += 1
                else:
                    pass

