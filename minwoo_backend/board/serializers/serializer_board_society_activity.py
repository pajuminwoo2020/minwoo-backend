import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardSocietyActivity

logger = logging.getLogger('logger')


class CreateBoardSocietyActivityRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardSocietyActivity


class BoardSocietyActivityRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardSocietyActivity


class BoardSocietyActivityResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardSocietyActivity

class BoardSocietyActivityWithBodyResponseSerializer(BoardSocietyActivityResponseSerializer):
    class Meta(BoardSocietyActivityResponseSerializer.Meta):
        fields = ['body'] + BoardSocietyActivityResponseSerializer.Meta.fields
