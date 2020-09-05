import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, get_image_pk, CategoryResponseSerializer
from board.models import BoardAction, Image

logger = logging.getLogger('logger')


class CreateBoardActionRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardAction
        fields = ['thumbnail_source', 'category'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardActionRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardAction
        fields = ['thumbnail_source', 'category'] + BoardBaseRequestSerializer.Meta.fields


class BoardActionResponseSerializer(BoardBaseResponseSerializer):
    category = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardAction
        fields = ['thumbnail_source', 'category'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=CategoryResponseSerializer)
    def get_category(self, obj):
        return CategoryResponseSerializer(obj.category).data


class BoardActionWithBodyResponseSerializer(BoardActionResponseSerializer):
    class Meta(BoardActionResponseSerializer.Meta):
        fields = ['body'] + BoardActionResponseSerializer.Meta.fields
