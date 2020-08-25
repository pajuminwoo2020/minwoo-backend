import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from information.models import About
from information.serializers import AboutResponseSerializer

logger = logging.getLogger('logger')

class AboutView(APIView):
    @swagger_auto_schema(
        tags=['about'],
        operation_id='Get About',
        responses={
            200: openapi.Schema(type=openapi.TYPE_STRING, description='{introduction: "", watchword: ""'),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets about
        """
        about = About.objects.order_by('created_at').last()

        if not about:
            return JsonResponse(None, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(AboutResponseSerializer(about).data, safe=False, status=status.HTTP_200_OK)
