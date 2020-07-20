import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, CategoryResponseSerializer
from board.models import BoardSocietyActivity

logger = logging.getLogger('logger')


class CreateBoardSocietyActivityRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardSocietyActivity
        fields = ['category'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardSocietyActivityRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardSocietyActivity
        fields = ['category'] + BoardBaseRequestSerializer.Meta.fields


class BoardSocietyActivityResponseSerializer(BoardBaseResponseSerializer):
    category = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardSocietyActivity
        fields = ['category'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=CategoryResponseSerializer)
    def get_category(self, obj):
        return CategoryResponseSerializer(obj.category).data

class BoardSocietyActivityWithBodyResponseSerializer(BoardSocietyActivityResponseSerializer):
    class Meta(BoardSocietyActivityResponseSerializer.Meta):
        fields = ['body'] + BoardSocietyActivityResponseSerializer.Meta.fields
