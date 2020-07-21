import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from information.models import InformationHistory
from information.serializers import InformationHistoryResponseSerializer
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator

logger = logging.getLogger('logger')

class InformationHistoriesView(ListModelMixin, APIView):
    ordering_default = ['-yyyymmdd']
    
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get InformationHistories',
        responses={
            200: SchemaGenerator.generate_page_schema(InformationHistoryResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of InformationHistories
        """
        return self.list(InformationHistory.objects.all(), InformationHistoryResponseSerializer)
