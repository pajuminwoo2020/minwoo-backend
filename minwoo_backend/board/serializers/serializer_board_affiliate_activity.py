import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardAffiliateActivity

logger = logging.getLogger('logger')


class CreateBoardAffiliateActivityRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardAffiliateActivity


class BoardAffiliateActivityRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardAffiliateActivity


class BoardAffiliateActivityResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardAffiliateActivity

class BoardAffiliateActivityWithBodyResponseSerializer(BoardAffiliateActivityResponseSerializer):
    class Meta(BoardAffiliateActivityResponseSerializer.Meta):
        fields = ['body'] + BoardAffiliateActivityResponseSerializer.Meta.fields
