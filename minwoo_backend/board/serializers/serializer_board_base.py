import logging
import re

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from user.serializers import UserResponseSerializer
from board.models import File

logger = logging.getLogger('logger')


def get_image_pk(path):
    if not path:
        return None

    thumbnail_pk_list = re.findall(r'\d+', path)
    if thumbnail_pk_list:
        return thumbnail_pk_list[0]

    return None


class CreateBoardBaseRequestSerializer(serializers.ModelSerializer):
    file_ids = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True, required=False, allow_null=True, allow_empty=True, source='files')

    class Meta:
        fields = ['title', 'body', 'file_ids']

    def validate(self ,data):
        user = self.context.get('user')
        data.update({'created_by': user})

        return data

    def create(self, validated_data):
        files = validated_data.pop('files', [])
        with transaction.atomic():
            instance =  super(CreateBoardBaseRequestSerializer, self).create(validated_data)
            for file_object in files:
                file_object.board_at = instance
                file_object.save()

            return instance


class BoardBaseRequestSerializer(serializers.ModelSerializer):
    file_ids = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True, required=False, allow_null=True, allow_empty=True, source='files')

    class Meta:
        fields = ['title', 'body', 'file_ids']
        extra_kwargs = {
            'title': {'required': False},
            'body': {'required': False},
            'file_ids': {'required': False},
        }

    def validate(self ,data):
        user = self.context.get('user')
        if not user.is_group_admin() and not user.is_group_staff() and self.instance and user != self.instance.created_by:
            raise serializers.ValidationError(_('The user does not have permission.'))

        return data

    def update(self, instance, validated_data):
        files = validated_data.pop('files', [])
        with transaction.atomic():
            instance =  super(BoardBaseRequestSerializer, self).update(instance, validated_data)
            files_for_delete = set(instance.files.all()).difference(set(files))
            files_for_insert = set(files).difference(set(instance.files.all()))
            for file_object in files_for_delete:
                file_object.delete()
            for file_object in files_for_insert:
                file_object.board_at = instance
                file_object.save()

            return instance


class BoardBaseResponseSerializer(serializers.ModelSerializer):
    hit_count = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'title', 'hit_count', 'created_by', 'files', 'created_at', 'updated_at']

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_hit_count(self, obj):
        return obj.hit_count.hits

    @swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    def get_created_by(self, obj):
        return UserResponseSerializer(obj.created_by).data

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_files(self, obj):
        from board.serializers import FileResponseSerializer

        return FileResponseSerializer(obj.files, many=True).data
