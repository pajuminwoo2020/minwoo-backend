import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardIntranetGeneral

logger = logging.getLogger('logger')


class CreateBoardIntranetGeneralRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardIntranetGeneral


class BoardIntranetGeneralRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardIntranetGeneral


class BoardIntranetGeneralResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardIntranetGeneral

class BoardIntranetGeneralWithBodyResponseSerializer(BoardIntranetGeneralResponseSerializer):
    class Meta(BoardIntranetGeneralResponseSerializer.Meta):
        fields = ['body'] + BoardIntranetGeneralResponseSerializer.Meta.fields
