from django.contrib import admin
from .models import LoginAttempt
from django.utils.translation import gettext_lazy as _

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
