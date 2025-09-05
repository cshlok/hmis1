from django.db import models
from core.models import TenantModel
import uuid
from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField


class PatientGender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    UNKNOWN = "UNKNOWN", "Unknown"


class Patient(TenantModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=16, choices=PatientGender.choices, default=PatientGender.UNKNOWN
    )
    phone = EncryptedCharField(max_length=128, blank=True)
    email = EncryptedEmailField(blank=True)
    address = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=255, blank=True)
    insurance_number = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["hospital", "last_name", "first_name"]),
            models.Index(fields=["uuid"]),
        ]
        unique_together = (
            ("hospital", "first_name", "last_name", "date_of_birth", "phone"),
        )
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"
