import logging
import re
from urllib.parse import quote

from django.http import JsonResponse, HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from information.models import Donation
from information.serializers import DonationResponseSerializer, DonationSimpleResponseSerializer, CreateDonationRequestSerializer
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import OrderingFilter

logger = logging.getLogger('logger')


class CreateDonationView(APIView):
    parser_classes = [MultiPartParser]

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
        donation.send_email_to_admin()

        return JsonResponse(DonationResponseSerializer(donation).data, safe=False, status=status.HTTP_200_OK)


class DonationDownloadView(APIView):
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Download Donation',
        responses={
            200: 'file',
        },
    )
    def get(self, request, uidb64, *args, **kwargs):
        """
        Gets a donation pdf file
        """
        uidb64_number = re.findall('\d+', force_text(urlsafe_base64_decode(uidb64)))
        donation_id = uidb64_number[0] if uidb64_number else '0'
        donation = get_object_or_404(Donation, pk=donation_id)
        file_name_quoted = quote(f'민우회 후원신청서_{donation.applicant_name}.pdf'.encode('utf-8'), safe='')

        response = HttpResponse(donation.generate_document(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name_quoted}"; filename*=UTF-8\'\'{file_name_quoted}'

        return response


class DonationsView(ListModelMixin, APIView):
    filter_backends = [OrderingFilter]
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Donations',
        responses={
            200: SchemaGenerator.generate_page_schema(DonationSimpleResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of Donations at the Institution with the corresponding id
        """
        return self.list(Donation.objects.all(), DonationSimpleResponseSerializer)
