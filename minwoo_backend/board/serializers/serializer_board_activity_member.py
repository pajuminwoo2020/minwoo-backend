import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, get_image_pk
from board.models import BoardActivityMember, Image

logger = logging.getLogger('logger')


class CreateBoardActivityMemberRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardActivityMember
        fields = ['thumbnail_source'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardActivityMemberRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardActivityMember
        fields = ['thumbnail_source'] + BoardBaseRequestSerializer.Meta.fields


class BoardActivityMemberResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardActivityMember
        fields = ['thumbnail_source'] + BoardBaseResponseSerializer.Meta.fields


class BoardActivityMemberWithBodyResponseSerializer(BoardActivityMemberResponseSerializer):
    class Meta(BoardActivityMemberResponseSerializer.Meta):
        fields = ['body'] + BoardActivityMemberResponseSerializer.Meta.fields
