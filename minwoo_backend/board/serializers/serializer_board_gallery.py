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
    thumbnail_source = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardGallery
        fields = ['thumbnail_source'] + CreateBoardBaseRequestSerializer.Meta.fields

    def create(self, validated_data):
        thumbnail_pk = get_image_pk(validated_data.pop('thumbnail_source', None))
        validated_data.update({
            'thumbnail': Image.objects.filter(pk=thumbnail_pk).first()
        })

        return super(CreateBoardGalleryRequestSerializer, self).create(validated_data)


class BoardGalleryRequestSerializer(BoardBaseRequestSerializer):
    thumbnail_source = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardGallery
        fields = ['thumbnail_source'] + BoardBaseRequestSerializer.Meta.fields

    def update(self, instance, validated_data):
        thumbnail_pk = get_image_pk(validated_data.pop('thumbnail_source', None))
        validated_data.update({
            'thumbnail': Image.objects.filter(pk=thumbnail_pk).first()
        })

        return super(BoardGalleryRequestSerializer, self).update(instance, validated_data)


class BoardGalleryResponseSerializer(BoardBaseResponseSerializer):
    thumbnail_source = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardGallery
        fields = ['thumbnail_source'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_thumbnail_source(self, obj):
        if obj.thumbnail:
            return reverse('board:image', kwargs={'image_id': obj.thumbnail.pk})

        return None


class BoardGalleryWithBodyResponseSerializer(BoardGalleryResponseSerializer):
    class Meta(BoardGalleryResponseSerializer.Meta):
        fields = ['body'] + BoardGalleryResponseSerializer.Meta.fields
