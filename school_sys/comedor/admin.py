from django.contrib import admin
from .models import CafeteriaAttendance


@admin.register(CafeteriaAttendance)
class CafeteriaAttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "date", "meal_type", "applied_price")
    list_filter = ("meal_type", "date")
    search_fields = ("student__name", "student__enrollment_number")
    date_hierarchy = "date"
    ordering = ("-date",)
