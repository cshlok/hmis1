from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from hospitals.models import HospitalPlan

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "hospital",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = getattr(user, "role", None)
        token["hospital"] = getattr(user, "hospital_id", None)
        # Include subscription module flags for convenience across services
        flags = [
            "enable_opd",
            "enable_ipd",
            "enable_diagnostics",
            "enable_pharmacy",
            "enable_accounting",
        ]
        hp = None
        try:
            if getattr(user, "hospital_id", None):
                hospital = getattr(user, "hospital", None)
                hp = getattr(hospital, "subscription", None)
                if hp is None:
                    hp = (
                        HospitalPlan.objects.select_related("plan")
                        .filter(hospital_id=user.hospital_id)
                        .first()
                    )
        except Exception:
            hp = None
        for f in flags:
            try:
                token[f] = bool(hp.is_enabled(f)) if hp else True
            except Exception:
                token[f] = True
        return token
