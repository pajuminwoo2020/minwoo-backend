import logging

from rest_framework import serializers

from information.models import HistoryBase

logger = logging.getLogger('logger')


class HistoryResponseSerializer(serializers.Serializer):
    memo = serializers.CharField()
    date_at = serializers.DateField()

    class Meta:
        fields = ['memo', 'date_at']


