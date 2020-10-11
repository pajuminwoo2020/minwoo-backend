from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from information.models import ClinicAbout

class ClinicAboutResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAbout
        fields = ['counseling', 'education', 'activity', 'counseling_image', 'education_image', 'activity_image', 'counseling_title', 'education_title', 'activity_title']
