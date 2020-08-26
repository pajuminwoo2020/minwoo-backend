import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from information.models import DonationPage
from information.serializers import DonationPageResponseSerializer

logger = logging.getLogger('logger')

class DonationPageView(APIView):
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Donation page',
        responses={
            200: DonationPageResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets Donation page
        """
        page = DonationPage.objects.order_by('created_at').last()

        if not page:
            return JsonResponse(None, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(DonationPageResponseSerializer(page).data, safe=False, status=status.HTTP_200_OK)
