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

    def validate(self ,data):
        user = self.context.get('user')
        data.update({'created_by': user})

        return data


class SocietyAboutRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyAbout
        fields = ['name', 'activity']
        extra_kwargs = {
            'name': {'required': False},
        }

    def validated(self ,data):
        user = self.context.get('user')
        if user != self.created_by:
            raise serializers.ValidationError(_('The user does not have permission.'))

        return data


class SocietyAboutResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    activity = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_name(self, obj):
        return obj.name

    @swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    def get_activity(self, obj):
        return UserResponseSerializer(obj.activity).data

    class Meta:
        model = SocietyAbout
        fields = ['id', 'name', 'activity']


class SocietyAboutWithBodyResponseSerializer(SocietyAboutResponseSerializer):
    class Meta(SocietyAboutResponseSerializer.Meta):
        fields = ['activity'] + SocietyAboutResponseSerializer.Meta.fields
