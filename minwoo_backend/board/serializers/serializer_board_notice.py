import logging
import os

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.urls import reverse
from django.conf import settings

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, get_image_pk, CategoryResponseSerializer
from board.models import BoardNotice

logger = logging.getLogger('logger')


class CreateBoardNoticeRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source', 'category'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardNoticeRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source', 'category'] + BoardBaseRequestSerializer.Meta.fields


class BoardNoticeResponseSerializer(BoardBaseResponseSerializer):
    category = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardNotice
        fields = ['thumbnail_source', 'category'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=CategoryResponseSerializer)
    def get_category(self, obj):
        return CategoryResponseSerializer(obj.category).data


class BoardNoticeWithBodyResponseSerializer(BoardNoticeResponseSerializer):
    class Meta(BoardNoticeResponseSerializer.Meta):
        fields = ['body'] + BoardNoticeResponseSerializer.Meta.fields
