import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import People

logger = logging.getLogger('logger')


class PeopleResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    position = serializers.CharField()
    job = serializers.CharField()

    class Meta:
        model = People
        fields = ['name', 'position', 'job']
