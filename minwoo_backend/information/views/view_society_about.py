import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from information.models import SocietyAbout
from information.serializers import SocietyAboutResponseSerializer
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator

logger = logging.getLogger('logger')


class SocietyAboutsView(ListModelMixin, APIView):
    @swagger_auto_schema(
        tags=['society_about'],
        operation_id='Get SocietyAbouts',
        operation_summary='✅✅',
        responses={
            200: SchemaGenerator.generate_page_schema(SocietyAboutResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of SocietyAbouts at the Institution with the corresponding id
        """
        return self.list(SocietyAbout.objects.all(), SocietyAboutResponseSerializer)
