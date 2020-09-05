import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from user.serializers import UserResponseSerializer
from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, get_image_pk
from board.models import BoardGallery, Image

logger = logging.getLogger('logger')


class CreateBoardGalleryRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardGallery
        fields = ['thumbnail_source'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardGalleryRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardGallery
        fields = ['thumbnail_source'] + BoardBaseRequestSerializer.Meta.fields


class BoardGalleryResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardGallery
        fields = ['thumbnail_source'] + BoardBaseResponseSerializer.Meta.fields


class BoardGalleryWithBodyResponseSerializer(BoardGalleryResponseSerializer):
    class Meta(BoardGalleryResponseSerializer.Meta):
        fields = ['body'] + BoardGalleryResponseSerializer.Meta.fields
