import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from hitcount.views import HitCountMixin

from information.models import People
from information.serializers import PeopleResponseSerializer
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')

class PeopleView(ListModelMixin, APIView):
    #filter_backends = [SearchFilter, OrderingFilter]
    #search_fields = ['created_by__fullname', 'title']
    #ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['people'],
        operation_id='Get Peoples',
        operation_summary='✅✅',
        responses={
            200: SchemaGenerator.generate_page_schema(PeopleResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardSettlementss at the Institution with the corresponding id
        """
        return self.list(People.objects.all(), PeopleResponseSerializer)
