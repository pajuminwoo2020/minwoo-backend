import logging

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
FRONT_HOST = 'http://tvenger.com'
SESSION_COOKIE_DOMAIN = ".tvenger.com"
CSRF_COOKIE_DOMAIN = ".tvenger.com"
CSRF_TRUSTED_ORIGINS = ['tvenger.com', 'api.tvenger.com', 'www.tvenger.com']
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
