from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import HealthSerializer

# Create your views here.


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(responses=OpenApiResponse(response=HealthSerializer))
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
            db_ok = row == (1,)
        except Exception:
            db_ok = False
        return Response({"status": "ok", "database": db_ok})
