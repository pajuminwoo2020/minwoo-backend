import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import SocietyAbout

logger = logging.getLogger('logger')


class SocietyAboutResponseSerializer(serializers.ModelSerializer):
    main_activity = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = SocietyAbout
        fields = ['id', 'name', 'description', 'main_activity', 'schedule', 'website', 'is_default']

    def _split_string(self, text):
        if not text:
            return []

        elem_list = text.strip().replace('\r', '').replace('\n', '').replace('\t', '').split('-')
        if not elem_list or len(elem_list) < 1:
            return []

        return elem_list[1:]


    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_main_activity(self, obj):
        return self._split_string(obj.main_activity)

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_schedule(self, obj):
        return self._split_string(obj.schedule)
