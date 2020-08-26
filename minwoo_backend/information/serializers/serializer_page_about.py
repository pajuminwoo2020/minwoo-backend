from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import About

class AboutResponseSerializer(serializers.Serializer):
    introduction = serializers.CharField()
    watchword = serializers.CharField()

    class Meta:
        model = About
        fields = ['introduction', 'watchword']
