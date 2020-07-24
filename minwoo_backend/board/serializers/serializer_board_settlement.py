import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.serializers import BoardBaseRequestSerializer, BoardBaseResponseSerializer, CreateBoardBaseRequestSerializer
from board.models import BoardSettlement

logger = logging.getLogger('logger')


class CreateBoardSettlementRequestSerializer(CreateBoardBaseRequestSerializer):
    class Meta(CreateBoardBaseRequestSerializer.Meta):
        model = BoardSettlement


class BoardSettlementRequestSerializer(BoardBaseRequestSerializer):

    class Meta(BoardBaseRequestSerializer.Meta):
        model = BoardSettlement


class BoardSettlementResponseSerializer(BoardBaseResponseSerializer):
    class Meta(BoardBaseResponseSerializer.Meta):
        model = BoardSettlement

class BoardSettlementWithBodyResponseSerializer(BoardSettlementResponseSerializer):
    class Meta(BoardSettlementResponseSerializer.Meta):
        fields = ['body'] + BoardSettlementResponseSerializer.Meta.fields
