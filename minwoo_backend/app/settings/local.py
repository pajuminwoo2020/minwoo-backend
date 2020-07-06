import sys

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += ['drf_yasg']
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv(BASE_DIR, 'db.sqlite3'),
    },
}

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
