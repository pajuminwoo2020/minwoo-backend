import logging

from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from information.models import Donation
from information.serializers import DonationResponseSerializer, CreateDonationRequestSerializer
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import OrderingFilter

logger = logging.getLogger('logger')


class CreateDonationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Create Donation',
        request_body=CreateDonationRequestSerializer,
        responses={
            200: DonationResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an Donation
        """
        serializer = CreateDonationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()

        return JsonResponse(DonationResponseSerializer(donation).data, safe=False, status=status.HTTP_200_OK)


class DonationView(APIView):
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Donation',
        responses={
            200: 'file',
        },
    )
    def get(self, request, donation_id, *args, **kwargs):
        """
        Gets a donation
        """
        from django.shortcuts import get_object_or_404
        donation = get_object_or_404(Donation, pk=donation_id)
        response = HttpResponse(donation.generate_document(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="hello"; filename*=UTF-8\'\'hello'

        return response


class DonationsView(ListModelMixin, APIView):
    filter_backends = [OrderingFilter]
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Donations',
        responses={
            200: SchemaGenerator.generate_page_schema(DonationResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of Donations at the Institution with the corresponding id
        """
        return self.list(Donation.objects.all(), DonationResponseSerializer)
