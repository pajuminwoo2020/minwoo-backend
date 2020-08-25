from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import About

class ClinicAboutResponseSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    activity = serializers.CharField()

    class Meta:
        model = About
        fields = ['purpose', 'activity']