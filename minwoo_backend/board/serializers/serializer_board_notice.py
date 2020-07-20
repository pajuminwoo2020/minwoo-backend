import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, get_image_pk, CategoryResponseSerializer
from board.models import BoardNotice, Image

logger = logging.getLogger('logger')


class CreateBoardNoticeRequestSerializer(CreateBoardBaseRequestSerializer):
    thumbnail_source = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source', 'category'] + CreateBoardBaseRequestSerializer.Meta.fields

    def create(self, validated_data):
        thumbnail_pk = get_image_pk(validated_data.pop('thumbnail_source', None))
        validated_data.update({
            'thumbnail': Image.objects.filter(pk=thumbnail_pk).first()
        })

        return super(CreateBoardNoticeRequestSerializer, self).create(validated_data)


class BoardNoticeRequestSerializer(BoardBaseRequestSerializer):
    thumbnail_source = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source', 'category'] + BoardBaseRequestSerializer.Meta.fields

    def update(self, instance, validated_data):
        thumbnail_pk = get_image_pk(validated_data.pop('thumbnail_source', None))
        validated_data.update({
            'thumbnail': Image.objects.filter(pk=thumbnail_pk).first()
        })

        return super(BoardNoticeRequestSerializer, self).update(instance, validated_data)


class BoardNoticeResponseSerializer(BoardBaseResponseSerializer):
    thumbnail_source = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source', 'category'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_thumbnail_source(self, obj):
        if obj.thumbnail:
            return reverse('board:image', kwargs={'image_id': obj.thumbnail.pk})

        return None

    @swagger_serializer_method(serializer_or_field=CategoryResponseSerializer)
    def get_category(self, obj):
        return CategoryResponseSerializer(obj.category).data


class BoardNoticeWithBodyResponseSerializer(BoardNoticeResponseSerializer):
    class Meta(BoardNoticeResponseSerializer.Meta):
        fields = ['body'] + BoardNoticeResponseSerializer.Meta.fields
