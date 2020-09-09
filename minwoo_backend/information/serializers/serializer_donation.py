import logging
from datetime import datetime

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.core.files import File

from information.models import Donation

logger = logging.getLogger('logger')


class CreateDonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            'donation_type', 'price', 'applicant_name', 'applicant_birthday', 'applicant_phone',
            'account_holder_name', 'account_holder_birthday', 'account_holder_phone',
            'email', 'bank_name', 'account_number', 'address', 'memo', 'resident_registration_number',
            'image_signature', 'agree_receipt', 'agree_unique', 'agree_personal', 'agree_offer',
            'agree_email', 'agree_newsletter', 'motivation',
        ]

    def create(self, validated_data):
        image_name = f'signature-{datetime.now().timestamp()}.png'
        validated_data.update({
            'image_signature': File(file=validated_data.get('image_signature').file, name=image_name),
        })

        return super(CreateDonationRequestSerializer, self).create(validated_data)


class DonationResponseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = [
            'id', 'donation_type', 'price', 'applicant_name', 'applicant_birthday', 'applicant_phone',
            'account_holder_name', 'account_holder_birthday', 'account_holder_phone',
            'email', 'bank_name', 'account_number', 'address', 'memo', 'resident_registration_number',
            'agree_receipt', 'agree_unique', 'agree_personal', 'agree_offer', 'absolute_url', 'created_at',
            'agree_email', 'agree_newsletter', 'motivation',
        ]

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class DonationSimpleResponseSerializer(serializers.ModelSerializer):
    applicant_name = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = ['id', 'donation_type', 'applicant_name', 'memo']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_applicant_name(self, obj):
        return obj.applicant_name[0] + ''.join(map(lambda x: '*', obj.applicant_name[1:]))
