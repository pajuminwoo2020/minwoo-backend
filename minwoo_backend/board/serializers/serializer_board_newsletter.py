import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, get_image_pk
from board.models import BoardNewsletter, Image

logger = logging.getLogger('logger')


class CreateBoardNewsletterRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardNewsletter
        fields = ['thumbnail_source'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardNewsletterRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardNewsletter
        fields = ['thumbnail_source'] + BoardBaseRequestSerializer.Meta.fields


class BoardNewsletterResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardNewsletter
        fields = ['thumbnail_source'] + BoardBaseResponseSerializer.Meta.fields


class BoardNewsletterWithBodyResponseSerializer(BoardNewsletterResponseSerializer):
    class Meta(BoardNewsletterResponseSerializer.Meta):
        fields = ['body'] + BoardNewsletterResponseSerializer.Meta.fields
