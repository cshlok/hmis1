from rest_framework import viewsets, permissions, decorators, response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta, time
from core.permissions import RolePermission, ModuleEnabledPermission
from .models import Appointment, AppointmentStatus
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.select_related("patient", "doctor", "hospital").all()
    filterset_fields = ["doctor", "patient", "status"]
    search_fields = ["reason", "notes"]
    ordering_fields = ["start_at", "end_at", "created_at"]
    permission_classes = [permissions.IsAuthenticated, ModuleEnabledPermission]
    required_module = "enable_opd"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or getattr(user, "role", None) == "SUPER_ADMIN":
            return qs
        if getattr(user, "hospital_id", None) is None:
            return qs.none()
        return qs.filter(hospital_id=user.hospital_id)

    def perform_create(self, serializer):
        user = self.request.user
        provided_hospital = serializer.validated_data.get("hospital")
        if not (
            user.is_superuser
            or getattr(user, "hospital_id", None)
            or getattr(user, "role", None) == "SUPER_ADMIN"
        ):
            raise PermissionDenied(
                "User must belong to a hospital to create appointments"
            )
        if (
            provided_hospital
            and not (user.is_superuser or user.role == "SUPER_ADMIN")
            and provided_hospital.id != user.hospital_id
        ):
            raise PermissionDenied("Cannot create appointment for another hospital")
        serializer.save(
            hospital_id=(
                provided_hospital.id if provided_hospital else user.hospital_id
            )
        )

    @decorators.action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated, RolePermission],
    )
    def complete(self, request, pk=None):
        self.allowed_roles = ["DOCTOR", "NURSE", "HOSPITAL_ADMIN"]
        appt = self.get_object()
        appt.status = AppointmentStatus.COMPLETED
        appt.save()
        # Generate bill if not exists
        try:
            from billing.models import Bill, BillLineItem, ServiceCatalog

            bill = Bill.objects.filter(appointment=appt).first()
            if bill is None:
                bill = Bill.objects.create(
                    hospital=appt.hospital, patient=appt.patient, appointment=appt
                )
                service = ServiceCatalog.objects.filter(
                    hospital=appt.hospital, code="CONSULT", active=True
                ).first()
                unit_price = service.price_cents if service else 0
                BillLineItem.objects.create(
                    hospital=appt.hospital,
                    bill=bill,
                    description="Consultation",
                    quantity=1,
                    unit_price_cents=unit_price,
                )
        except Exception:
            pass
        return response.Response(AppointmentSerializer(appt).data)

    @decorators.action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated, RolePermission],
    )
    def cancel(self, request, pk=None):
        self.allowed_roles = ["DOCTOR", "NURSE", "HOSPITAL_ADMIN"]
        appt = self.get_object()
        appt.status = AppointmentStatus.CANCELLED
        appt.save()
        return response.Response(AppointmentSerializer(appt).data)

    @decorators.action(detail=False, methods=["get"])
    def available_slots(self, request):
        self.throttle_scope = "slots"
        # Params: doctor (id), date=YYYY-MM-DD
        doctor_id = request.query_params.get("doctor")
        date_str = request.query_params.get("date")
        if not (doctor_id and date_str):
            return response.Response(
                {"detail": "doctor and date are required"}, status=400
            )
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return response.Response({"detail": "Invalid date"}, status=400)
        slot_minutes = settings.DEFAULT_APPOINTMENT_SLOT_MINUTES
        # Get roster shift times for the doctor (if any), else default 9-17
        from hr.models import DutyRoster

        roster = (
            DutyRoster.objects.filter(user_id=doctor_id, date=target_date)
            .select_related("shift")
            .first()
        )
        if roster and roster.shift:
            start_t: time = roster.shift.start_time
            end_t: time = roster.shift.end_time
        else:
            start_t = time(9, 0)
            end_t = time(17, 0)
        # Build list of candidate slots and exclude overlaps
        tz = timezone.get_current_timezone()
        start_dt = timezone.make_aware(datetime.combine(target_date, start_t), tz)
        end_dt = timezone.make_aware(datetime.combine(target_date, end_t), tz)
        slots = []
        current = start_dt
        existing = Appointment.objects.filter(
            doctor_id=doctor_id,
            start_at__date=target_date,
            status__in=[AppointmentStatus.SCHEDULED, AppointmentStatus.COMPLETED],
        ).values_list("start_at", "end_at")
        while current + timedelta(minutes=slot_minutes) <= end_dt:
            next_dt = current + timedelta(minutes=slot_minutes)
            overlap = False
            for s, e in existing:
                if s < next_dt and e > current:
                    overlap = True
                    break
            if not overlap and current > timezone.now():
                slots.append(
                    {"start_at": current.isoformat(), "end_at": next_dt.isoformat()}
                )
            current = next_dt
        return response.Response(
            {"doctor": int(doctor_id), "date": date_str, "slots": slots}
        )
