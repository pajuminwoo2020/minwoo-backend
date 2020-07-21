import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from information.models import People

logger = logging.getLogger('logger')
class PeopleResponseSerializer(serializers.ModelSerializer):


    class Meta:
        model = People
        fields = ['id', 'name', 'position', 'department']