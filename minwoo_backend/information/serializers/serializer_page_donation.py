from rest_framework import serializers

from information.models import DonationPage

class DonationPageResponseSerializer(serializers.Serializer):
    introduction = serializers.CharField()

    class Meta:
        model = DonationPage
        fields = ['introduction']
