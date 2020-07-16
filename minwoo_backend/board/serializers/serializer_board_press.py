import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardPress

logger = logging.getLogger('logger')


class CreateBoardPressRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardPress


class BoardPressRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardPress


class BoardPressResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardPress

class BoardPressWithBodyResponseSerializer(BoardPressResponseSerializer):
    class Meta(BoardPressResponseSerializer.Meta):
        fields = ['body'] + BoardPressResponseSerializer.Meta.fields
