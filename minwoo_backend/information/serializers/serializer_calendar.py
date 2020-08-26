import logging

from drf_yasg.utils import swagger_serializer_method
from django.utils.timezone import localtime
from django.utils.dateformat import format
from rest_framework import serializers

from information.models import Calendar

logger = logging.getLogger('logger')


class CalendarSimpleResponseSerializer(serializers.ModelSerializer):
    schedule_from = serializers.SerializerMethodField()
    schedule_to = serializers.SerializerMethodField()

    class Meta:
        model = Calendar
        fields = ['id', 'schedule_name', 'schedule_from', 'schedule_to']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_schedule_from(self, obj):
        return localtime(obj.schedule_from).date()

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_schedule_to(self, obj):
        return localtime(obj.schedule_to).date()


class CalendarResponseSerializer(serializers.ModelSerializer):
    schedule_from = serializers.SerializerMethodField()
    schedule_to = serializers.SerializerMethodField()

    class Meta:
        model = Calendar
        fields = ['id', 'schedule_name', 'schedule_from', 'schedule_to', 'memo']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_schedule_from(self, obj):
        return localtime(obj.schedule_from).strftime('%Y-%m-%d %H:%M')

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_schedule_to(self, obj):
        return localtime(obj.schedule_to).strftime('%Y-%m-%d %H:%M')


class CreateScheduleRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ['schedule_name', 'schedule_from', 'schedule_to', 'memo']
