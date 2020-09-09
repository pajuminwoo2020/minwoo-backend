import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer, CategoryResponseSerializer
from board.models import BoardAffiliateActivity

logger = logging.getLogger('logger')


class CreateBoardAffiliateActivityRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardAffiliateActivity
        fields = ['thumbnail_source', 'category', 'on_board_action'] + CreateBoardBaseRequestSerializer.Meta.fields


class BoardAffiliateActivityRequestSerializer(BoardBaseRequestSerializer):
    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardAffiliateActivity
        fields = ['thumbnail_source', 'category', 'on_board_action'] + BoardBaseRequestSerializer.Meta.fields


class BoardAffiliateActivityResponseSerializer(BoardBaseResponseSerializer):
    category = serializers.SerializerMethodField()

    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardAffiliateActivity
        fields = ['thumbnail_source', 'category', 'on_board_action'] + BoardBaseResponseSerializer.Meta.fields

    @swagger_serializer_method(serializer_or_field=CategoryResponseSerializer)
    def get_category(self, obj):
        return CategoryResponseSerializer(obj.category).data

class BoardAffiliateActivityWithBodyResponseSerializer(BoardAffiliateActivityResponseSerializer):
    class Meta(BoardAffiliateActivityResponseSerializer.Meta):
        fields = ['body'] + BoardAffiliateActivityResponseSerializer.Meta.fields
