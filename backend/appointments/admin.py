from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "hospital", "start_at", "end_at", "status")
    list_filter = ("hospital", "doctor", "status")
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "doctor__username",
        "reason",
    )
    autocomplete_fields = ("patient", "doctor", "hospital")
