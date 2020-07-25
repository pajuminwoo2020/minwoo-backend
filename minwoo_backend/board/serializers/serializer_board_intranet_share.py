import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardIntranetShare

logger = logging.getLogger('logger')


class CreateBoardIntranetShareRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardIntranetShare


class BoardIntranetShareRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardIntranetShare


class BoardIntranetShareResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardIntranetShare

class BoardIntranetShareWithBodyResponseSerializer(BoardIntranetShareResponseSerializer):
    class Meta(BoardIntranetShareResponseSerializer.Meta):
        fields = ['body'] + BoardIntranetShareResponseSerializer.Meta.fields
