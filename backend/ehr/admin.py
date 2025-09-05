from django.contrib import admin
from .models import Encounter, EncounterNote


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "hospital", "appointment", "is_finalized")
    list_filter = ("hospital", "doctor", "is_finalized")
    search_fields = ("patient__first_name", "patient__last_name", "doctor__username")
    autocomplete_fields = ("patient", "doctor", "hospital", "appointment")


@admin.register(EncounterNote)
class EncounterNoteAdmin(admin.ModelAdmin):
    list_display = ("encounter", "author", "created_at")
    search_fields = ("content",)
    autocomplete_fields = ("encounter", "author")
