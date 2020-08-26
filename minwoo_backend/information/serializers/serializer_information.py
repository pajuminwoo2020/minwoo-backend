import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import Information

logger = logging.getLogger('logger')


class InformationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = [
            'membership_management', 'membership_management_email', 'membership_management_phone',\
            'chief_executive', 'address_street', 'address_jibun', 'location_subway', 'location_bus', 'location_car', \
            'registration_number', 'email', 'phone', 'fax', 'bank_account', 'phone_counseling', 'webhost_counseling', 'instagram_feed',
        ]
