from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LoginAttempt
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin personalizado para el modelo User con soporte para roles."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    ordering = ['email']
    list_display = ['email', 'role', 'is_staff', 'activo', 'last_login']
    list_filter = ['role', 'is_staff', 'activo']
    search_fields = ['email', 'nombre']
    
    # Fieldsets para edición de usuario existente
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información Personal'), {'fields': ('nombre', 'role')}),
        (_('Permisos'), {
            'fields': ('activo', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('MFA Debug'), {'fields': ('mfa_code', 'mfa_expires_at')}),
        (_('Fechas Importantes'), {'fields': ('last_login',)}),
    )
    
    # Fieldsets para creación de usuario (add_form)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'nombre', 'password', 'confirm_password'),
        }),
    )

    # Indicar campos que son read-only si es necesario
    readonly_fields = ('last_login',)


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'timestamp', 'was_successful', 'get_status_display')
    list_filter = ('was_successful', 'timestamp')
    search_fields = ('email', 'ip_address')
    readonly_fields = ('email', 'ip_address', 'timestamp', 'was_successful')
    ordering = ('-timestamp',)

    def get_status_display(self, obj):
        return "Exitoso" if obj.was_successful else "Fallido"
    get_status_display.short_description = "Estado"
    get_status_display.admin_order_field = 'was_successful'

    def has_add_permission(self, request):
        return False  # Solo lectura, son logs del sistema

    def has_change_permission(self, request, obj=None):
        return False  # No se deben modificar los logs

    def has_delete_permission(self, request, obj=None):
        return True   # Permitir borrar si es necesario limpiar logs
