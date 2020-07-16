import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import Banner

logger = logging.getLogger('logger')


class BannerResponseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['href', 'absolute_url', 'banner_type']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_absolute_url(self, obj):
        return obj.get_image_absolute_url()
