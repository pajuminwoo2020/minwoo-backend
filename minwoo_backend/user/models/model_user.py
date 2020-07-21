import logging

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.utils import translation
from django.utils.translation import activate, LANGUAGE_SESSION_KEY
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


logger = logging.getLogger('logger')

# password_reset_token = PasswordResetTokenGenerator()

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
    GROUP_STAFF = "스태프"
    GROUP_ADMIN = "관리자"

    userid = models.EmailField(max_length=255, unique=True, blank=False)
    fullname = models.CharField(max_length=255, blank=False)
    fullname_en = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=5, null=False, blank=False, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    timezone = models.CharField(max_length=255, null=False, blank=False, choices=settings.TIME_ZONES, default=settings.TIME_ZONE_ASIA_SEOUL)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = '사용자 관리'

    def __str__(self):
        return f'[pk={self.pk}, userid={self.userid}]'

    def get_fullname(self):
        current_language = translation.get_language()  # returns currently selected language code (None if translations are deactivated or when None is passed to override())
        if current_language is not None and 'en' in current_language:
            name_en = self.fullname_en
            if name_en is not None and name_en.strip() != '':
                logger.info(f'Getting english name from User={self}')

                return self.fullname_en
            else:
                logger.info(f'No english name available from User={self}')

        logger.info(f'Getting local name from User={self}')

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
