import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import InformationHistory

logger = logging.getLogger('logger')

class InformationHistoryResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationHistory
        fields = ['id', 'year', 'body']


