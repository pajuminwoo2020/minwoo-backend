import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from information.models import ClinicAbout
from information.serializers import ClinicAboutResponseSerializer

logger = logging.getLogger('logger')

class ClinicAboutView(APIView):
    @swagger_auto_schema(
        tags=['clinic_about'],
        operation_id='Get Clinic About',
        responses={
            200: openapi.Schema(type=openapi.TYPE_STRING, description='{purpose: "", activity: ""'),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets about
        """
        clinic_about = ClinicAbout.objects.order_by('created_at').last()

        if not clinic_about:
            return JsonResponse(None, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(ClinicAboutResponseSerializer(clinic_about).data, safe=False, status=status.HTTP_200_OK)