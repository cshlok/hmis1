from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    HOSPITAL_ADMIN = "HOSPITAL_ADMIN", "Hospital Admin"
    DOCTOR = "DOCTOR", "Doctor"
    NURSE = "NURSE", "Nurse"
    PHARMACIST = "PHARMACIST", "Pharmacist"
    RECEPTIONIST = "RECEPTIONIST", "Receptionist"
    LAB_TECH = "LAB_TECH", "Lab Technician"
    BILLING_CLERK = "BILLING_CLERK", "Billing Clerk"


class User(AbstractUser):
    role = models.CharField(
        max_length=32,
        choices=UserRole.choices,
        default=UserRole.RECEPTIONIST,
    )
    hospital = models.ForeignKey(
        "hospitals.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
