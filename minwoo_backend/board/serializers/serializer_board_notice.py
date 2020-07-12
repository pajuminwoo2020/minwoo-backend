import logging
import re

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardNotice, Image

logger = logging.getLogger('logger')


def _get_image_pk(path):
    thumbnail_pk_list = re.findall(r'\d+', path)
    if thumbnail_pk_list:
        return thumbnail_pk_list[0]

    return None


class CreateBoardNoticeRequestSerializer(CreateBoardBaseRequestSerializer):
    thumbnail_source = serializers.CharField(required=False, allow_blank=True)

    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source'] + CreateBoardBaseRequestSerializer.Meta.fields

    def create(self, validated_data):
        thumbnail_pk = _get_image_pk(validated_data.pop('thumbnail_source', None))
        validated_data.update({
            'thumbnail': Image.objects.filter(pk=thumbnail_pk).first()
        })

        return  super(CreateBoardNoticeRequestSerializer, self).create(validated_data)


class BoardNoticeRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardNotice


class BoardNoticeResponseSerializer(BoardBaseResponseSerializer):
    thumbnail_source = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_thumbnail_source(self, obj):
        if obj.thumbnail:
            return reverse('board:image', kwargs={'image_id': obj.thumbnail.pk})

        return None


class BoardNoticeWithBodyResponseSerializer(BoardNoticeResponseSerializer):
    class Meta(BoardNoticeResponseSerializer.Meta):
        fields = ['body'] + BoardNoticeResponseSerializer.Meta.fields
