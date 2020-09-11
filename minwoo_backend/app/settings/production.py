import logging

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DOMAIN = os.getenv('DOMAIN')
ALLOWED_HOSTS = ['*']
FRONT_HOST = f'http://${DOMAIN}'
SESSION_COOKIE_DOMAIN = f".${DOMAIN}"
CSRF_COOKIE_DOMAIN = f".${DOMAIN}"
CSRF_TRUSTED_ORIGINS = [f'${DOMAIN}', f'api.${DOMAIN}', f'www.${DOMAIN}']
SESSION_COOKIE_SECURE = False #TODO 수정
CSRF_COOKIE_SECURE = False    #TODO 수정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'minwoo_db'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': '5432',
        'TEST': {
            'NAME': os.getenv('DB_TEST', ''),
        },
    },
}
