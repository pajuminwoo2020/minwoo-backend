import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import Information, DonationButtonImage, AffiliateButtonImage

logger = logging.getLogger('logger')


class InformationResponseSerializer(serializers.ModelSerializer):
    donation_url = serializers.SerializerMethodField()
    affiliate_url = serializers.SerializerMethodField()

    class Meta:
        model = Information
        fields = [
            'membership_management', 'membership_management_email', 'membership_management_phone',\
            'chief_executive', 'address_street', 'address_jibun', 'location_subway', 'location_bus', 'location_car', \
            'registration_number', 'email', 'phone', 'fax', 'bank_account', 'instagram_feed',\
            'location_latitude', 'location_longitude', 'donation_url', 'affiliate_url',
        ]

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_donation_url(self, obj):
        image = DonationButtonImage.objects.all().order_by('-created_at').first()
        if not image:
            return ''

        return image.get_image_absolute_url()

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_affiliate_url(self, obj):
        image = AffiliateButtonImage.objects.all().order_by('-created_at').first()
        if not image:
            return ''

        return image.get_image_absolute_url()
