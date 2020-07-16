import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardActivityMember

logger = logging.getLogger('logger')


class CreateBoardActivityMemberRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardActivityMember


class BoardActivityMemberRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardActivityMember


class BoardActivityMemberResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardActivityMember

class BoardActivityMemberWithBodyResponseSerializer(BoardActivityMemberResponseSerializer):
    class Meta(BoardActivityMemberResponseSerializer.Meta):
        fields = ['body'] + BoardActivityMemberResponseSerializer.Meta.fields
