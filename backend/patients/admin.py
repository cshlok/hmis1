from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "hospital", "date_of_birth", "active")
    search_fields = ("last_name", "first_name", "phone", "email")
    list_filter = ("hospital", "active", "gender")
    autocomplete_fields = ("hospital",)
