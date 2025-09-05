from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import TenantModel


class AppointmentStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class Appointment(TenantModel):
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=16,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED,
    )
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["hospital", "doctor", "start_at"]),
            models.Index(fields=["hospital", "patient", "start_at"]),
        ]
        ordering = ["start_at"]

    def clean(self):
        if self.end_at <= self.start_at:
            raise ValidationError("end_at must be after start_at")
        # basic overlap check for same doctor in same hospital excluding cancelled
        qs = Appointment.objects.filter(
            hospital=self.hospital,
            doctor=self.doctor,
            status__in=[AppointmentStatus.SCHEDULED, AppointmentStatus.COMPLETED],
        ).exclude(pk=self.pk)
        qs = qs.filter(start_at__lt=self.end_at, end_at__gt=self.start_at)
        if qs.exists():
            raise ValidationError("Overlapping appointment for this doctor")

    def __str__(self) -> str:
        return (
            f"{self.patient} with {self.doctor} at {timezone.localtime(self.start_at)}"
        )
