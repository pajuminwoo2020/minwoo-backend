import logging

from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.serializers import UserCreateRequestSerializer, UserRequestSerializer, UserResponseSerializer, UserLoginRequestSerializer, PasswordResetRequestSerializer, PasswordChangeRequestSerializer, PasswordUpdateRequestSerializer
from app.common.mixins import PermissionMixin
from app.exceptions import ErrorCode
from user.models import user_activation_token, password_reset_token

logger = logging.getLogger('logger')


class CreateUserView(APIView):
    @swagger_auto_schema(
        tags=['user'],
        operation_id='Create User',
        request_body=UserCreateRequestSerializer,
        responses={
            200: UserResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates a User
        """
        if request.user.is_authenticated:
            return JsonResponse({'error_message': _('Already logged in')}, safe=False, status=status.HTTP_400_BAD_REQUEST)

        userid = request.data.get('userid')
        if get_user_model().objects.filter(userid=userid).exists():
            # 중복아이디 났을때 프론트에서 리다이렉트 처리할 수 있도록 validation전에 미리 체크함. 이번 프로젝트에만 임시로 넣은 코드
            logger.info(f'Attempted to create User with existing userid={userid}')

            return JsonResponse({'error_code': ErrorCode.USERID_ALREADY_EXISTS}, safe=False, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user_serializer = UserCreateRequestSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            user.send_activation_email()

        return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    @swagger_auto_schema(
        tags=['user'],
        operation_id='Login User',
        request_body=UserLoginRequestSerializer,
        responses={
            200: UserResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Login a User.
        """
        user_serializer = UserLoginRequestSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        user = authenticate(userid=request.data.get('userid'), password=request.data.get('password'))
        if not request.data.get('is_remember'):
            request.session.set_expiry(0) # Expire session at browser close
        login(request, user)
        user.activate_language(request)

        logger.info(f'Successfully logged in User={user}')

        return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['user'],
        operation_id='Logout User',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Logout the User within the current request.
        """
        user_id = request.user.id
        logout(request)

        return JsonResponse({'id': user_id}, safe=False, status=status.HTTP_200_OK)


class UserView(PermissionMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated],
    }

    @swagger_auto_schema(
        tags=['user'],
        operation_id='Get User',
        responses={
            200: UserResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets the User within the current request.
        """
        if not request.user.is_authenticated:
            return JsonResponse(None, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(UserResponseSerializer(request.user).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['user'],
        operation_id='Update User',
        request_body=UserRequestSerializer,
        responses={
            200: UserResponseSerializer,
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Updates the User within the current request.
        """
        user_serializer = UserRequestSerializer(data=request.data, instance=request.user)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.activate_language(request)

        return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['user'],
        operation_id='Password Change (whiled logged in)',
        request_body=PasswordChangeRequestSerializer,
        responses={
            200: UserResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Changes the requesting User's password.
        """
        user = request.user
        password_reset_serializer = PasswordChangeRequestSerializer(data=request.data, instance=user)
        password_reset_serializer.is_valid(raise_exception=True)
        password_reset_serializer.save()

        # prevent the password change from logging out the session
        update_session_auth_hash(request, user)

        return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)


class UserActivationView(APIView):
    @swagger_auto_schema(
        tags=['user'],
        operation_id='Activate User',
        responses={
            200: UserResponseSerializer,
        },
    )
    def post(self, request, uidb64, token):
        user = get_user_model().objects.filter(pk=force_text(urlsafe_base64_decode(uidb64))).first()

        if user is not None and user_activation_token.check_token(user, token):
            user.activate()
            logger.info(f'Successfully activate User={user}')

            return JsonResponse(UserResponseSerializer(user).data, safe=False, status = status.HTTP_200_OK)

        return JsonResponse({'error_message': _('Failed to activate user')}, safe=False, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
     @swagger_auto_schema(
         tags=['user'],
         operation_id='Password Reset',
         request_body=PasswordResetRequestSerializer,
         responses={
             200: UserResponseSerializer,
         },
     )
     def post(self, request, *args, **kwargs):
         """
         Requests an email for resetting the password
         """
         password_reset_serializer = PasswordResetRequestSerializer(data=request.data)
         password_reset_serializer.is_valid(raise_exception=True)
         user = get_user_model().objects.filter(userid=password_reset_serializer.validated_data.get('userid')).first()
         if user is None:
            return JsonResponse({'error_message': _('Failed Request')}, safe=False, status=status.HTTP_400_BAD_REQUEST)

         user.send_password_reset_email()

         return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)


class PasswordUpdateView(APIView):
    @swagger_auto_schema(
        tags=['user'],
        operation_id='Password Update',
        request_body=PasswordUpdateRequestSerializer,
        responses={
            200: UserResponseSerializer,
        },
    )
    def post(self, request, uidb64, token, *args, **kwargs):
        """
        Confirms a password reset with a new password
        """
        user = get_user_model().objects.filter(pk=force_text(urlsafe_base64_decode(uidb64))).first()

        if user is not None and password_reset_token.check_token(user, token):
            logger.info(f'Password update link confirmed for User={user}')

            password_update_serializer = PasswordUpdateRequestSerializer(data=request.data, instance=user)

            password_update_serializer.is_valid(raise_exception=True)
            password_update_serializer.reset_password(user)

            logger.info('Successfully updated. Please login with the new password.')

            return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse({'error_message': _('Failed to update password')}, safe=False, status=status.HTTP_400_BAD_REQUEST)
