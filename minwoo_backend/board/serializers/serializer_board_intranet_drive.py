import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardIntranetDrive

logger = logging.getLogger('logger')


class CreateBoardIntranetDriveRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardIntranetDrive


class BoardIntranetDriveRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardIntranetDrive


class BoardIntranetDriveResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardIntranetDrive

class BoardIntranetDriveWithBodyResponseSerializer(BoardIntranetDriveResponseSerializer):
    class Meta(BoardIntranetDriveResponseSerializer.Meta):
        fields = ['body'] + BoardIntranetDriveResponseSerializer.Meta.fields
