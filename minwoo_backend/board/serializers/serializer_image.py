import logging

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from board.models import Image

logger = logging.getLogger('logger')


class UploadImageRequestSerializer(serializers.ModelSerializer):
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
    file = serializers.ImageField(source='image_file')

    class Meta:
        model = Image
        fields = ['file']

    def validate(self, data):
        file = data.get('image_file')
        if file.size > UploadImageRequestSerializer.MAX_UPLOAD_SIZE:
            logger.warning('Raising error for request where image size limit has exceeded')

            raise serializers.ValidationError({'image_file': _('Each file size cannot exceed 50MB.')})

        return data


class ImageResponseSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['location']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_location(self, obj):
        return obj.get_image_absolute_url()
