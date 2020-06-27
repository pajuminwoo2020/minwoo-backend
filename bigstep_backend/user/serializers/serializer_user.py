import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import get_default_password_validators
from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

logger = logging.getLogger('quotalogger')


def _validate_password(password, password_field=None):
    """
    Validate whether the password meets all validator requirements.

    :param password: the password to validate
    :return: None if the password is valid,
             ValidationError with all error messages otherwise.
    """
    errors = []
    password_validators = get_default_password_validators()  # within settings.AUTH_PASSWORD_VALIDATORS

    if password is None or len(password.strip()) <= 0:
        raise serializers.ValidationError({'password': 'Invalid password'})

    for validator in password_validators:
        try:
            validator.validate(password, None)
        except serializers.ValidationError as error:
            errors.append(error)
    if errors:
        raise serializers.ValidationError(errors if password_field is None else {password_field: errors})


class UserCreateRequestSerializer(serializers.ModelSerializer):
    fullname_local = serializers.CharField(source='fullname', trim_whitespace=True)

    class Meta:
        model = get_user_model()
        fields = ['userid', 'password', 'fullname_local', 'fullname_en']

    def validate(self, data):
        _validate_password(data['password'], 'password')

        return data

    def create(self, validated_data):
        return get_user_model().objects.create(
            userid=validated_data.get('userid'),
            fullname=validated_data.get('fullname'),
            fullname_en=validated_data.get('fullname_en'),
            password=validated_data.get('password'),
            is_active=True,
        )

    def update(self, instance, validated_data):
        raise ValueError('Cannot update with UserCreateRequestSerializer')


class UserRequestSerializer(serializers.ModelSerializer):
    fullname_local = serializers.CharField(source='fullname', required=False, trim_whitespace=True)
    language = serializers.ChoiceField(choices=settings.LANGUAGES, required=False)

    class Meta:
        model = get_user_model()
        fields = ['userid', 'fullname_local', 'fullname_en', 'language', 'timezone']
        extra_kwargs = {
            'userid': {'required': False},
        }

    def validate(self, data):
        user = self.instance
        if user is None:
            raise serializers.ValidationError(_('The user for the info to change is empty'))

        if not user.is_active:
            raise serializers.ValidationError(_('The user for the info to change is not active'))

        userid = data.get('userid', None)

        return data

    def create(self, validated_data):
        raise NotImplementedError


class UserResponseSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['userid', 'fullname', 'fullname_en', 'language', 'timezone', 'last_login']

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_fullname(self, obj):
        return obj.get_fullname()


class UserLoginRequestSerializer(serializers.Serializer):
    userid = serializers.EmailField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, write_only=True)
    is_remember = serializers.BooleanField(required=True)

    class Meta:
        fields = ['userid', 'password', 'is_remember']

    def validate(self, data):
        user = get_user_model().objects.filter(userid=data.get('userid', None)).first()
        if not user:
            raise serializers.ValidationError({'userid': _('Incorrect email')})
        if not user.check_password(data.get('password', None)):
            raise serializers.ValidationError({'password': _('Incorrect password')})
        if not user.is_active:
            raise serializers.ValidationError({'userid': _('Inactive user')})

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
