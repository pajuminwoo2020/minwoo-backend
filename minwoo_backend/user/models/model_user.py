import logging

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.utils import six, translation
from django.utils.translation import activate, LANGUAGE_SESSION_KEY
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.template.loader import render_to_string

from app.common.utils import send_email

logger = logging.getLogger('logger')


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):  # overriding default
        login_timestamp = '' if (user is None or user.last_login is None) else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
                six.text_type(user.pk if user is not None else 0) + six.text_type(user.userid if user is not None else '') + six.text_type(user.is_active if user is not None else False) +
                six.text_type(login_timestamp) + six.text_type(timestamp)
        )

user_activation_token = UserActivationTokenGenerator()
password_reset_token = PasswordResetTokenGenerator()


class UserManager(BaseUserManager):
    def create_user(self, userid, fullname, password, is_active=False, fullname_en=None):
        if not userid:
            raise ValueError('User must have a userid')
        if not fullname:
            raise ValueError('User must have a fullname')
        if not password:
            raise ValueError('User must have a password')

        if User.objects.filter(userid=userid).exists():
            logger.info(f'Attempted to create User with existing userid={userid}')

            return User.objects.get(userid=userid)

        user = self.model(
            userid=userid,
            fullname=fullname,
            is_active=is_active,
        )
        if fullname_en is not None and fullname_en.strip() != '':
            user.fullname_en = fullname_en
        user.set_password(password)
        user.save(using=self._db)
        logger.info(f'Created new User={user}')

        return user

    def create_superuser(self, userid, password):
        """
        Creates and saves a superuser with the given params.
        """
        user = self.create_user(
            userid,
            password=password,
            fullname='Admin',
            is_active=True,
        )
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    GROUP_STAFF = "활동가"
    GROUP_ADMIN = "관리자"
    GROUP_GENERAL = "일반 사용자"

    userid = models.EmailField(max_length=255, unique=True, blank=False, verbose_name='아이디')
    fullname = models.CharField(max_length=255, blank=False, verbose_name='이름')
    fullname_en = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=5, null=False, blank=False, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    timezone = models.CharField(max_length=255, null=False, blank=False, choices=settings.TIME_ZONES, default=settings.TIME_ZONE_ASIA_SEOUL)
    is_active = models.BooleanField(default=False, verbose_name='이메일 인증여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = '사용자 관리'
        verbose_name = '사용자 관리'

    def __str__(self):
        return f'[pk={self.pk}, userid={self.userid}]'

    def get_fullname(self):
        current_language = translation.get_language()  # returns currently selected language code (None if translations are deactivated or when None is passed to override())
        if current_language is not None and 'en' in current_language:
            name_en = self.fullname_en
            if name_en is not None and name_en.strip() != '':
                return self.fullname_en
            else:
                logger.info(f'No english name available from User={self}')

        return self.fullname

    def set_userid(self, userid):
        self.userid = userid
        self.save()
        logger.info(f'User={self} updated to have userid={self.userid}')

        return self

    def activate(self):
        self.is_active = True
        self.save()
        logger.info(f'Activated User={self}')

        return self

    def activate_language(self, request):
        request.session[LANGUAGE_SESSION_KEY] = self.language
        activate(self.language)

        return self

    def is_group_admin(self):
        if self.is_superuser:
            return True

        for group in self.groups.all():
            if group.name == User.GROUP_ADMIN:
                return True

        return False

    def is_group_staff(self):
        for group in self.groups.all():
            if group.name == User.GROUP_STAFF:
                return True

        return False

    def has_perm(self, perm, obj=None):  # used by Django's admin
        return self.is_group_admin()

    def has_module_perms(self, app_label):  # used by Django's admin
        return self.is_group_admin()

    @property
    def is_staff(self):  # used by Django's admin
        return self.is_group_admin()

    def get_groups(self):
        group_list = []

        if self.is_group_admin():
            group_list.append(User.GROUP_ADMIN)
        elif self.is_group_staff():
            group_list.append(User.GROUP_STAFF)
        else:
            group_list.append(User.GROUP_GENERAL)

        return group_list

    def send_activation_email(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = user_activation_token.make_token(self)
        message = render_to_string('user_activation_email.html', {
            'handle_url': f'{settings.FRONT_HOST}{reverse("user:activate", kwargs={"uidb64": uidb64, "token": token})}',
            'user': self,
        })
        mail_subject = '[민우회] 회원가입 인증 메일입니다.'
        send_email(
            subject=mail_subject,
            body=message,
            to=[self.userid]
        )

    def send_password_reset_email(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = password_reset_token.make_token(self)
        message = render_to_string('password_reset_email.html', {
            'handle_url': f'{settings.FRONT_HOST}{reverse("user:password_update", kwargs={"uidb64": uidb64, "token": token})}',
            'user': self,
        })
        mail_subject = '[민우회] 패스워드 재설정 메일입니다.'

        send_email(
            subject=mail_subject,
            body=message,
            to=[self.userid]
        )

    def send_email_to_admin(self):
        """
        민우회 관리자 이메일로 회원가입 알림을 보냄
        """
        from information.models import Information

        information = Information.objects.all().first()
        mail_subject = f'[파주여성민우회] 새로운 회원({self.fullname})이 가입했습니다.'

        send_email(
            subject=mail_subject,
            body=f'새로운 회원({self.fullname}[{self.userid}])이 가입했습니다.',
            to=[information.membership_management_email if information else ''],
        )
