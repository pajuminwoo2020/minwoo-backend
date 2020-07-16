import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from information.models import Banner
from information.serializers import BannerResponseSerializer
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator

logger = logging.getLogger('logger')


class BannersView(ListModelMixin, APIView):

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Banners',
        responses={
            200: SchemaGenerator.generate_page_schema(BannerResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of Banners
        """
        return self.list(Banner.objects.all(), BannerResponseSerializer)
