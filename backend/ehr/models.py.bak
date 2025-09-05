from django.db import models
from core.models import TenantModel, TimeStampedModel


class Encounter(TenantModel):
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="encounters"
    )
    doctor = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="encounters"
    )
    appointment = models.OneToOneField(
        "appointments.Appointment", on_delete=models.SET_NULL, null=True, blank=True
    )
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription_text = models.TextField(blank=True)
    is_finalized = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Encounter for {self.patient}"


class EncounterNote(TimeStampedModel):
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name="notes"
    )
    author = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    content = models.TextField()

    def __str__(self) -> str:
        return f"Note {self.pk} for Encounter {self.encounter_id}"


def encounter_attachment_upload_to(instance, filename: str) -> str:
    return f"encounters/{instance.encounter_id}/{filename}"


class EncounterAttachment(TimeStampedModel):
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, related_name="attachments"
    )
    uploaded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to=encounter_attachment_upload_to)
    description = models.CharField(max_length=255, blank=True)
