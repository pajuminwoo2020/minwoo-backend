import logging

from rest_framework import serializers

from board.models import Category

logger = logging.getLogger('logger')


class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
