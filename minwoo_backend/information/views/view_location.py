import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from hitcount.views import HitCountMixin

from information.models import InformationLocation
from information.serializers import InformationLocationSerializer
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')

class IntroLocationView(APIView):
    @swagger_auto_schema(
        tags=['location'],
        operation_id='Get Location',
        responses={
            200: InformationLocationSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets the Location within the current request.
        """
        ##if not request.user.is_authenticated:
        ##    return JsonResponse(None, safe=False, status=status.HTTP_200_OK)
        ##location = get_list_or_404(InformationLocation)
        location = InformationLocation.objects.first()
        # InformationLocation.objects.first(),   InformationLocation.object.all().first()
        return JsonResponse(InformationLocationSerializer(location).data, safe=False, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
        tags=['location'],
        operation_id='Update Location',
        request_body=InformationLocationSerializer,
        responses={
            200: InformationLocationSerializer,
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Updates the Location within the current request.
        """
        location_serializer = InformationLocationSerializer(data=request.data)
        location_serializer.is_valid(raise_exception=True)
        location = location_serializer.save()
        ##user.activate_language(request)

        return JsonResponse(location_serializer.data, safe=False, status=status.HTTP_200_OK)
