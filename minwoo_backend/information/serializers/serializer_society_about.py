import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from user.serializers import UserResponseSerializer
from information.models import SocietyAbout

logger = logging.getLogger('logger')


class CreateSocietyAboutRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyAbout
        fields = ['name', 'activity']


class SocietyAboutRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyAbout
        fields = ['name', 'activity']
        extra_kwargs = {
            'name': {'required': False},
        }

class SocietyAboutResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyAbout
        fields = ['id', 'name', 'activity']


class SocietyAboutWithBodyResponseSerializer(SocietyAboutResponseSerializer):
    class Meta(SocietyAboutResponseSerializer.Meta):
        fields = SocietyAboutResponseSerializer.Meta.fields
