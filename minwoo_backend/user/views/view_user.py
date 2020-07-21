import logging

from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.serializers import UserCreateRequestSerializer, UserRequestSerializer, UserResponseSerializer, UserLoginRequestSerializer, PasswordResetRequestSerializer
from app.common.mixins import PermissionMixin
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from app.settings import base

#인증 메일 발송 구현
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from user.tokens import account_activation_token
from user.models import User

logger = logging.getLogger('logger')
password_reset_token = PasswordResetTokenGenerator()

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
        
        message = render_to_string('account_activate_email.html', {
            'user': user,
            #나중에 frontend로
            'domain': 'localhost:3000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })

        mail_subject = '[민우회] 회원가입 인증 메일입니다.'

        to_email = user.userid
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return JsonResponse(UserResponseSerializer(user).data, safe=False, status=status.HTTP_200_OK)

class UserActivateView(APIView):
    def get(self, request, uidb64, token):
        user = User.objects.get(pk=force_text(urlsafe_base64_decode(uidb64)))

        if user is not None and account_activation_token.check_token(user, token):
            user.activate()

            logger.info(f'Successfully activate User={user}')
            return JsonResponse(UserResponseSerializer(user).data, safe=False, status = status.HTTP_200_OK)

        #에러 메시지?
        return JsonResponse({'error_message': _('Failed to activate user')}, safe=False, status=status.HTTP_400_BAD_REQUEST)

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


class PasswordResetView(APIView):

     @swagger_auto_schema(
         tags=['user'],
         operation_id='Password Reset',
         operation_summary='✅✅',
         request_body=PasswordResetRequestSerializer,
         responses={
             200: UserResponseSerializer,
         },
     )

     #post가 아닌 일반 함수로 처리하면?
     def post(self, request, *args, **kwargs):
         """
         Requests an email for resetting the password
         """
         password_reset_serializer = PasswordResetRequestSerializer(data=request.data)
         password_reset_serializer.is_valid(raise_exception=True)
           
         # send reset email
         #profile = password_reset_serializer.get_profile()
         #if profile is None:
         #    return JsonResponse({'error_message': _('Failed Request')}, safe=False, status=status.HTTP_400_BAD_REQUEST)
         #profile.send_password_reset_email()

        #  user = password_reset_serializer.get_user()
        #  if user is None:
        #      return JsonResponse({'error_message': _('Failed Request')}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        #  user.send_password_reset_email()

        #  return JsonResponse(UserResponseSerializer(profile.user).data, safe=False, status=status.HTTP_200_OK)

         #인자로 뭐 넘겨야하는지...token genarator는 어떤거 써야하는지
         #uidb64 = urlsafe_base64_encode(force_bytes(user_id))
         #token = password_reset_token.make_token(user_id)

         #handle_url = f'{settings.WEBAPP_HOST}{reverse("board:board_settlement_create", kwargs={"uidb64": uidb64, "token": token})}'
         handle_url = 'www.naver.com'

         subject = '[민우회] 비밀번호 재설정 안내 메일입니다.'
         message = '아래 주소로 이동하여 비밀번호를 재설정해주시기 바랍니다.\
                     본 메일을 수신한 뒤라도 위 링크를 통해 비밀번호를 재설정 하지 않으면, 비밀번호가 변경되지 않습니다.\
                     회원님께서 비밀번호 재설정을 요청하지 않았는데 본 메일을 수신하셨다면 chanyoung_kim@tmax.co.kr로 연락 주시기 바랍니다.'
         
         #유저 이메일 뽑아오는 올바른 방법?
         userid = password_reset_serializer.get_userid()

         send_mail(
         subject,
         message,
         base.EMAIL_HOST_USER,
         [userid],
         fail_silently=False,
         )

        #  send_mail(
        #  '민우회 비밀번호 재설정 이메일',
        #  '아래 링크를 클릭해서 비밀번호를 재설정 해주세요',
        #  'cykim0315@gamil.com',
        #  ['chanyoung_kim@tmax.co.kr'],
        #  fail_silently=False,
        #  )

        #어떤 response보내줘야 하는지??
         return JsonResponse(UserResponseSerializer(userid, context={'request': request}).data, safe=False, status=status.HTTP_200_OK)

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
