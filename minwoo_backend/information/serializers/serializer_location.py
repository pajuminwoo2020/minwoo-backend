import logging

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from user.serializers import UserResponseSerializer
from information.models import InformationLocation

logger = logging.getLogger('logger')

class InformationLocationRequestSerializer(serializers.ModelSerializer):
    ## Meta는 serializer 를 사용했을 시, serialize 할 데이터들을 의미하는 것 같은디....
    class Meta:
        model = InformationLocation
        ##fields = ['title', 'body']
        ##extra_kwargs = {
        ##    'title': {'required': False},
        ##}

    def validated(self ,data):
        #user = self.context.get('user')
        #if user != self.created_by:
        #    raise serializers.ValidationError(_('The user does not have permission.'))

        return data

class InformationLocationSerializer(serializers.ModelSerializer):
    ##hit_count = serializers.SerializerMethodField()
    ##created_by = serializers.SerializerMethodField()

    ##@swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    ##def get_hit_count(self, obj):
    ##    return obj.hit_count.hits

    ##@swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    ##def get_created_by(self, obj):
    ##    return UserResponseSerializer(obj.created_by).data

    class Meta:
        model = InformationLocation
        fields = ['location_name', 'location_roadname', 'location_lotnumber', 'byTrain', 'byBus', 'byCar']