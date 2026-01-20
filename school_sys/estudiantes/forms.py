from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Estudiante

User = get_user_model()

class EstudianteCreationForm(forms.ModelForm):
    """
    Formulario personalizado para la creación de estudiantes desde el Admin.
    Permite crear el Usuario (User) y el Estudiante simultáneamente.
    """
    # Campos extra para la creación del Usuario
    email_usuario = forms.EmailField(
        required=True, 
        label="Email del Usuario",
        help_text="Correo electrónico para el login del estudiante"
    )
    username_usuario = forms.CharField(
        required=False, 
        label="Username (opcional)",
        help_text="Nombre de usuario opcional para el login"
    )
    password_usuario = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Contraseña del Usuario",
        help_text="Contraseña para el acceso al sistema"
    )
    
    class Meta:
        model = Estudiante
        exclude = ('usuario', 'matricula') # Campos automáticos
        
    def save(self, commit=True):
        if not commit:
            # Si commit es False, retornamos la instancia con el usuario asignado si ya existe,
            # pero como es creación, necesitamos crear el usuario sí o sí.
            # En el flujo del admin, save() se llama usualmente con commit=True,
            # o save_model lo maneja. 
            pass

        # Usamos atomic para asegurar que ambos se crean o ninguno
        with transaction.atomic():
            # 1. Crear el Usuario asociado
            user = User.objects.create_user(
                email=self.cleaned_data['email_usuario'],
                username=self.cleaned_data.get('username_usuario') or None,
                password=self.cleaned_data['password_usuario'],
                nombre=self.cleaned_data.get('nombre', ''),
                role='estudiante'  # Rol correcto para estudiantes
            )
            
            # 2. Asignar el usuario a la instancia de Estudiante
            self.instance.usuario = user
            
            # 3. Guardar Estudiante
            estudiante = super().save(commit=commit)
            
        return estudiante
