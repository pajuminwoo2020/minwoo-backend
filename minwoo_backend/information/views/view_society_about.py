import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from information.models import SocietyAbout
from information.serializers import SocietyAboutResponseSerializer, CreateSocietyAboutRequestSerializer, SocietyAboutRequestSerializer, SocietyAboutWithBodyResponseSerializer
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter

logger = logging.getLogger('logger')


class CreateSocietyAboutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['society_about'],
        operation_id='Create Society About',
        operation_summary='✅✅',
        request_body=CreateSocietyAboutRequestSerializer,
        responses={
            200: SocietyAboutResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an SocietyAbout
        """
        serializer = CreateSocietyAboutRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        society_about = serializer.save()

        return JsonResponse(SocietyAboutResponseSerializer().data, safe=False, status=status.HTTP_200_OK)


class SocietyAboutView(PermissionMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated],
        'delete': [IsAuthenticated],
    }

    @swagger_auto_schema(
        tags=['society_about'],
        operation_id='Get SocietyAbout',
        operation_summary='✅✅',
        responses={
            200: SocietyAboutWithBodyResponseSerializer,
        },
    )
    def get(self, request, society_about_id, *args, **kwargs):
        """
        Gets the SocietyAbout with the corresponding id
        """
        society_about = get_object_or_404(SocietyAbout, pk=society_about_id)

        return JsonResponse(SocietyAboutWithBodyResponseSerializer(society_about).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['society_about'],
        operation_id='Update SocietyAbout',
        operation_summary='✅✅',
        request_body=SocietyAboutRequestSerializer,
        responses={
            200: SocietyAboutResponseSerializer,
        },
    )
    def put(self, request, society_about_id, *args, **kwargs):
        """
        Updates the SocietyAbout with the corresponding id
        """
        society_about = get_object_or_404(SocietyAbout, pk=society_about_id)

        serializer = SocietyAboutRequestSerializer(data=request.data, instance=society_about, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        society_about = serializer.save()

        return JsonResponse(SocietyAboutResponseSerializer(society_about).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['society_about'],
        operation_id='Delete SocietyAbout',
        operation_summary='✅✅',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
        },
    )
    def delete(self, request, society_about_id, *args, **kwargs):
        """
        Deletes the SocietyAbout with the corresponding id """
        society_about = get_object_or_404(SocietyAbout, pk=society_about_id)
        if request.user != society_about.created_by:
            return JsonResponse({'error_message': _('The user does not have permission.')}, status=status.HTTP_400_BAD_REQUEST)

        society_about.delete()

        return JsonResponse({'id': society_about_id}, safe=False, status=status.HTTP_200_OK)


class SocietyAboutsView(ListModelMixin, APIView):
    filter_backends = [SearchFilter]
    search_fields = ['name']

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
