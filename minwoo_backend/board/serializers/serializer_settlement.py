import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from board.models import BoardSettlement

logger = logging.getLogger('logger')


class CreateBoardSettlementRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardSettlement
        fields = ['title', 'body']

    def validated(self ,data):
        user = self.context.get('user')
        data.update({'created_by': user})

        return data


class BoardSettlementRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardSettlement
        fields = ['title', 'body']
        extra_kwargs = {
            'title': {'required': False},
        }

    def validated(self ,data):
        user = self.context.get('user')
        if user != self.created_by:
            raise serializers.ValidationError(_('The user does not have permission.'))

        return data


class BoardSettlementResponseSerializer(serializers.ModelSerializer):
    hit_count = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_hit_count(self, obj):
        return obj.hit_count.hits

    class Meta:
        model = BoardSettlement
        fields = ['id', 'title', 'body', 'hit_count', 'created_by', 'created_at', 'updated_at']
