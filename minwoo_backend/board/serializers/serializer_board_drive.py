import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardDrive

logger = logging.getLogger('logger')


class CreateBoardDriveRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardDrive


class BoardDriveRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardDrive


class BoardDriveResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardDrive

class BoardDriveWithBodyResponseSerializer(BoardDriveResponseSerializer):
    class Meta(BoardDriveResponseSerializer.Meta):
        fields = ['body'] + BoardDriveResponseSerializer.Meta.fields
