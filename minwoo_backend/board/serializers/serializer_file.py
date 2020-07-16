import logging

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from board.models import File

logger = logging.getLogger('logger')


class UploadFileRequestSerializer(serializers.ModelSerializer):
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB

    class Meta:
        model = File
        fields = ['file']

    def validate(self, data):
        file = data.get('file')
        if file.size > UploadFileRequestSerializer.MAX_UPLOAD_SIZE:
            logger.warning('Raising error for request where file size limit has exceeded')

            raise serializers.ValidationError({'file': _('Each file size cannot exceed 50MB.')})

        return data

    def create(self, validated_data):
        file = validated_data.get('file')
        validated_data.update({
            'file_name': file.name,
        })

        return super(UploadFileRequestSerializer, self).create(validated_data)


class FileResponseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'file_name', 'absolute_url']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
