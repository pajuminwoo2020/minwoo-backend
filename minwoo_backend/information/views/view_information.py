import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from information.models import Information
from information.serializers import InformationResponseSerializer

logger = logging.getLogger('logger')


class InformationView(APIView):
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Information',
        responses={
            200: InformationResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets the information
        """
        information = Information.objects.all().first()

        return JsonResponse(InformationResponseSerializer(information).data, safe=False, status=status.HTTP_200_OK)
