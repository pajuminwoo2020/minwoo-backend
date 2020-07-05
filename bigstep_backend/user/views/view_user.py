import logging

from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.serializers import UserCreateRequestSerializer, UserRequestSerializer, UserResponseSerializer, UserLoginRequestSerializer
from app.common.mixins import PermissionMixin

logger = logging.getLogger('quotalogger')


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

        user_serializer = UserCreateRequestSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

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

        return JsonResponse(UserResponseSerializer(user, context={'request': request}).data, safe=False, status=status.HTTP_200_OK)


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

        return JsonResponse(UserResponseSerializer(request.user, context={'request': request}).data, safe=False, status=status.HTTP_200_OK)

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

        return JsonResponse(UserResponseSerializer(user, context={'request': request}).data, safe=False, status=status.HTTP_200_OK)
