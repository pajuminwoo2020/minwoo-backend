import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardMemberSpace

logger = logging.getLogger('logger')


class CreateBoardMemberSpaceRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardMemberSpace


class BoardMemberSpaceRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardMemberSpace


class BoardMemberSpaceResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardMemberSpace

class BoardMemberSpaceWithBodyResponseSerializer(BoardMemberSpaceResponseSerializer):
    class Meta(BoardMemberSpaceResponseSerializer.Meta):
        fields = ['body'] + BoardMemberSpaceResponseSerializer.Meta.fields
