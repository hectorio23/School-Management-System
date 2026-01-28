from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import (
    Estudiante, Inscripcion, Grupo, CicloEscolar, 
    EstadoEstudiante, HistorialEstadosEstudiante
)

User = get_user_model()

class EstudianteCreationForm(forms.ModelForm):
    """Formulario para creacion de estudiante con usuario e inscripcion inicial"""
    
    # Credenciales
    email_usuario = forms.EmailField(
        required=True, 
        label="Email del Usuario"
    )
    username_usuario = forms.CharField(
        required=True, 
        label="Username / CURP"
    )
    password_usuario = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Contraseña"
    )

    # Inscripcion
    ciclo_escolar = forms.ModelChoiceField(
        queryset=CicloEscolar.objects.all(),
        required=True,
        label="Ciclo Escolar"
    )
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=True,
        label="Grupo"
    )
    
    class Meta:
        model = Estudiante
        fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'direccion')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ciclo_activo = CicloEscolar.objects.filter(activo=True).first()
        if ciclo_activo:
            self.fields['ciclo_escolar'].initial = ciclo_activo
            self.fields['grupo'].queryset = Grupo.objects.filter(ciclo_escolar=ciclo_activo).select_related('grado', 'grado__nivel_educativo')

    def save(self, commit=True):
        with transaction.atomic():
            # 1. Crear el Usuario
            user = User.objects.create_user(
                email=self.cleaned_data['email_usuario'],
                username=self.cleaned_data['username_usuario'],
                password=self.cleaned_data['password_usuario'],
                nombre=f"{self.cleaned_data['nombre']} {self.cleaned_data['apellido_paterno']}",
                role='estudiante',
                is_staff=False,
                is_superuser=False
            )
            
            self.instance.usuario = user
            
            def save_academic_data():
                # 2. Inscripcion
                Inscripcion.objects.create(
                    estudiante=self.instance,
                    grupo=self.cleaned_data['grupo'],
                    ciclo_escolar=self.cleaned_data['ciclo_escolar'],
                    estatus='activo'
                )
                
                # 3. Estado
                estado_activo = EstadoEstudiante.objects.filter(nombre__iexact='ACTIVO').first()
                if estado_activo:
                    HistorialEstadosEstudiante.objects.create(
                        estudiante=self.instance,
                        estado=estado_activo,
                        justificacion="Alta automatica"
                    )

            if commit:
                estudiante = super().save(commit=True)
                save_academic_data()
            else:
                estudiante = super().save(commit=False)
                self.save_m2m = save_academic_data
                
        return estudiante



