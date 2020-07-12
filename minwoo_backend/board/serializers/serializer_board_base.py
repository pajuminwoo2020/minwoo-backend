import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer

logger = logging.getLogger('logger')


class CreateBoardBaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'body']

    def validate(self ,data):
        user = self.context.get('user')
        data.update({'created_by': user})

        return data


class BoardBaseRequestSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['title', 'body']
        extra_kwargs = {
            'title': {'required': False},
            'body': {'required': False},
        }

    def validate(self ,data):
        user = self.context.get('user')
        if self.instance and user != self.instance.created_by:
            raise serializers.ValidationError(_('The user does not have permission.'))

        return data


class BoardBaseResponseSerializer(serializers.ModelSerializer):
    hit_count = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'hit_count', 'created_by', 'created_at', 'updated_at']

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_hit_count(self, obj):
        return obj.hit_count.hits

    @swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    def get_created_by(self, obj):
        return UserResponseSerializer(obj.created_by).data
