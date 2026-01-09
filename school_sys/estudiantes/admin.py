from django.contrib import admin
from .models import (
    Grade, Group, Student, Tutor, StudentTutor,
    StudentStatus, StudentStatusHistory,
    Stratum, StratumHistory, SocioeconomicEvaluation
)


# ==========================================
# ADMIN DE ENTIDADES INDIVIDUALES (CRUD)
# ==========================================

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level")
    search_fields = ("name", "level")
    ordering = ("level", "name")
    verbose_name = "Grado"
    verbose_name_plural = "Grados"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "generation", "grade", "created_at")
    search_fields = ("name", "generation")
    list_filter = ("grade",)
    ordering = ("grade", "name")
    verbose_name = "Grupo"
    verbose_name_plural = "Grupos"


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "paternal_surname",
        "maternal_surname",
        "phone",
        "email",
    )
    search_fields = ("name", "paternal_surname", "maternal_surname")
    ordering = ("paternal_surname",)
    verbose_name = "Tutor"
    verbose_name_plural = "Tutores"


@admin.register(StudentStatus)
class StudentStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    verbose_name = "Estado del Estudiante"
    verbose_name_plural = "Estados del Estudiante"


@admin.register(Stratum)
class StratumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "discount_percentage", "active")
    actions = ["assign_stratum_to_students"]

    def assign_stratum_to_students(self, request, queryset):
        stratum = queryset.first()
        if not stratum:
            self.message_user(request, "No se seleccionó ningún estrato.")
            return

        # FILTROS BÁSICOS QUE PUEDES EXPANDIR
        students = Student.objects.filter(
            group__grade__name__icontains=request.GET.get("grade", ""),
            group__name__icontains=request.GET.get("group", ""),
            name__icontains=request.GET.get("name", "")
        )

        count = 0
        for s in students:
            s.current_stratum = stratum
            s.save()
            count += 1

        self.message_user(request, f"Estrato asignado a {count} estudiantes.")

    assign_stratum_to_students.short_description = (
        "Asignar estrato a estudiantes"
    )



@admin.register(SocioeconomicEvaluation)
class SocioeconomicEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "monthly_income",
        "suggested_stratum",
        "date"
    )
    list_filter = ("suggested_stratum", "date")
    ordering = ("-date",)
    verbose_name = "Evaluación Socioeconómica"
    verbose_name_plural = "Evaluaciones Socioeconómicas"

    def save(self, *args, **kwargs):

        # lógica para sugerir estrato
        score = 0

        # ingresos
        if self.monthly_income < 8000:
            score += 3
        elif self.monthly_income < 12000:
            score += 2
        else:
            score += 1

        # número de integrantes
        if self.number_of_members >= 6:
            score += 3
        elif self.number_of_members >= 4:
            score += 2
        else:
            score += 1

        # vivienda
        if "rentada" in self.housing_type.lower():
            score += 2
        else:
            score += 1

        # seleccionamos estrato según score
        if score >= 7:
            self.suggested_stratum = Stratum.objects.get(name="Estrato 1")
        elif score >= 5:
            self.suggested_stratum = Stratum.objects.get(name="Estrato 2")
        else:
            self.suggested_stratum = Stratum.objects.get(name="Estrato 3")

        super().save(*args, **kwargs)


@admin.register(StratumHistory)
class StratumHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "stratum", "date")
    list_filter = ("stratum", "date")
    ordering = ("-date",)
    verbose_name = "Historial de Estrato"
    verbose_name_plural = "Historiales de Estrato"


@admin.register(StudentStatusHistory)
class StudentStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "status", "date")
    list_filter = ("status", "date")
    ordering = ("-date",)
    verbose_name = "Historial de Estado"
    verbose_name_plural = "Historiales de Estado"


# ==========================================
# INLINES PARA USARSE SOLO EN STUDENTADMIN
# ==========================================

class TutorCreateInline(admin.StackedInline):
    model = Tutor
    extra = 1

class StudentTutorInline(admin.TabularInline):
    model = StudentTutor
    extra = 1

class TutorInline(admin.TabularInline):
    model = StudentTutor
    extra = 1


class StratumHistoryInline(admin.TabularInline):
    model = StratumHistory
    extra = 0
    readonly_fields = ("date",)


class StudentStatusHistoryInline(admin.TabularInline):
    model = StudentStatusHistory
    extra = 0
    readonly_fields = ("date",)


class EvaluationInline(admin.TabularInline):
    model = SocioeconomicEvaluation
    extra = 1


# ==========================================
# ADMIN CENTRALIZADO PARA STUDENT
# ==========================================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    # ORGANIZA LAS SECCIONES DEL FORMULARIO
    fieldsets = (
        ("Información General", {
            "fields": (
                "enrollment_number",
                "name",
                "paternal_surname",
                "maternal_surname",
                "address",
                "group",
            )
        }),
        ("Cuenta de Usuario", {
            "fields": ("username", "password", "key_digest")
        }),
        ("Estado Escolar", {
            "fields": ("current_status", "current_stratum")
        }),
    )

    # INLINES
    inlines = [
        TutorInline,
        EvaluationInline,
        StratumHistoryInline,
        StudentStatusHistoryInline,
        StudentTutorInline,      # Enlazar tutor al estudiante
    ]

    list_display = (
        "enrollment_number",
        "name",
        "paternal_surname",
        "maternal_surname",
        "group",
        "current_status",
        "current_stratum",
    )

    search_fields = (
        "enrollment_number",
        "name",
        "paternal_surname",
        "maternal_surname"
    )


