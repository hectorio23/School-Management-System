from django.contrib import admin
from django import forms

ADMISSION_MODULE = True

from .models import (
    AdmissionUser, AdmissionTutor, Aspirante, 
    AdmissionTutorAspirante
)

if ADMISSION_MODULE:
    
    # Formulario personalizado para AdmissionUser
    class AdmissionUserForm(forms.ModelForm):
        class Meta:
            model = AdmissionUser
            fields = ('email', 'password')
        
        def save(self, commit=True):
            instance = super().save(commit=False)
            
            # Generar el folio automáticamente si es un nuevo usuario
            if not instance.pk:
                ultimo_folio = AdmissionUser.objects.all().order_by('-folio').first()
                if ultimo_folio:
                    instance.folio = ultimo_folio.folio + 1
                else:
                    instance.folio = 2000
            
            if commit:
                instance.save()
            return instance
    
    # Formulario personalizado para Aspirante
    class AspiranteForm(forms.ModelForm):
        class Meta:
            model = Aspirante
            fields = '__all__'
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Filtrar solo usuarios que NO tienen aspirante asignado
            usuarios_ocupados = Aspirante.objects.values_list('user_id', flat=True)
            
            # Si estamos editando, incluir el usuario actual
            if self.instance.pk and self.instance.user:
                self.fields['user'].queryset = AdmissionUser.objects.exclude(
                    folio__in=usuarios_ocupados
                ).union(
                    AdmissionUser.objects.filter(folio=self.instance.user.folio)
                )
            else:
                # Si es nuevo, solo mostrar usuarios disponibles
                self.fields['user'].queryset = AdmissionUser.objects.exclude(
                    folio__in=usuarios_ocupados
                )
    
    # Inline para agregar/crear tutores directamente
    class TutorAspiranteInline(admin.TabularInline):
        model = AdmissionTutorAspirante
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores del Aspirante"
        fields = ('tutor', 'parentesco')
        extra = 1
        autocomplete_fields = ['tutor']
    
    # Admin principal del Aspirante
    class AdmisionAspirante(admin.ModelAdmin):
        form = AspiranteForm
        list_display = ("get_folio", "nombre", "apellido_paterno", "apellido_materno", "get_email")
        search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'user__folio', 'user__email')
        list_filter = ('user__is_active', 'user__is_verified')
        
        inlines = [TutorAspiranteInline]
        
        fieldsets = (
            ('Usuario de Autenticación', {
                'fields': ('user',)
            }),
            ('Información Personal', {
                'fields': ('nombre', 'apellido_paterno', 'apellido_materno')
            }),
        )
        
        def get_folio(self, obj):
            return obj.user.folio if obj.user else None
        get_folio.short_description = 'Folio'
        get_folio.admin_order_field = 'user__folio'
        
        def get_email(self, obj):
            return obj.user.email if obj.user else None
        get_email.short_description = 'Email'
        get_email.admin_order_field = 'user__email'
    
    # Admin para AdmissionUser
    class AdmissionUserAdmin(admin.ModelAdmin):
        form = AdmissionUserForm
        list_display = ('folio', 'email', 'is_active', 'is_verified', 'date_joined')
        list_filter = ('is_active', 'is_verified')
        search_fields = ('folio', 'email')
        readonly_fields = ('folio', 'date_joined')
        
        fieldsets = (
            ('Credenciales', {
                'fields': ('folio', 'email', 'password')
            }),
            ('Estado', {
                'fields': ('is_active', 'is_verified', 'date_joined')
            }),
        )
        
        # Solo mostrar folio, email y password en el formulario de creación
        def get_fields(self, request, obj=None):
            if obj:  # Editando
                return ('folio', 'email', 'password', 'is_active', 'is_verified', 'date_joined')
            else:  # Creando
                return ('email', 'password')
    
    # Admin para Tutores
    class AdmissionTutorAdmin(admin.ModelAdmin):
        list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'numero_telefono')
        search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'email')
    
    # Registros
    admin.site.register(Aspirante, AdmisionAspirante)
    admin.site.register(AdmissionUser, AdmissionUserAdmin)
    admin.site.register(AdmissionTutor, AdmissionTutorAdmin)
    admin.site.register(AdmissionTutorAspirante)