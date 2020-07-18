import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import Donation

logger = logging.getLogger('logger')


class CreateDonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donation_type', 'price', 'period', 'user_name', 'birthday', 'phone', 'email', 'bank_account', 'address']


class DonationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donation_type', 'price', 'period', 'user_name', 'birthday', 'phone', 'email', 'bank_account', 'address']
