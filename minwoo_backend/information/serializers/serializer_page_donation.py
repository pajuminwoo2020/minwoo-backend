from rest_framework import serializers

from information.models import DonationPage

class DonationPageResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonationPage
        fields = ['introduction', 'benefits', 'payment_method']
