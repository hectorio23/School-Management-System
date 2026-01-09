from django.contrib import admin
from .models import PaymentConcept, Debt, Payment


@admin.register(PaymentConcept)
class PaymentConceptAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_amount", "educational_level")
    search_fields = ("name", "educational_level")
    ordering = ("name",)


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "concept",
        "amount",
        "generation_date",
        "due_date",
        "applied_surcharge",
        "paid",
    )
    list_filter = ("paid", "concept")
    search_fields = ("student__name", "student__enrollment_number")
    date_hierarchy = "generation_date"
    ordering = ("-generation_date",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "debt", "amount", "date", "method")
    list_filter = ("method", "date")
    search_fields = ("debt__student__name",)
    date_hierarchy = "date"
    ordering = ("-date",)
