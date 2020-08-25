import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = environ.Path(__file__) - 1
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'templates')
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), 'static')
LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'logs')
MEDIA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'media')

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env_file = str(SETTINGS_DIR.path('.env'))
env.read_env(env_file)

# Environment variable: "development" or "production"
ENV = env.str('DJANGO_SETTINGS_MODULE', 'local').split('.')[-1]
IS_ENV_LOCAL = (ENV == 'local')
IS_ENV_PRODUCTION = (ENV == 'production')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# Session Serializer
# https://stackoverflow.com/questions/24229397/django-object-is-not-json-serializable-error-after-upgrading-django-to-1-6-5
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'hitcount',
    'user',
    'board',
    'information',

]

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.TimeZoneMiddleware',
    'app.middleware.LoggerMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

ASGI_APPLICATION = 'app.channels_router.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LOCALE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'locale')
LOCALE_PATHS = [LOCALE_DIR]
LANGUAGE_KO_KR = 'ko-KR'
LANGUAGE_EN_US = 'en-US'
LANGUAGES = [
    (LANGUAGE_KO_KR, 'Korean'),
    (LANGUAGE_EN_US, 'English'),
]
LANGUAGE_CODE = LANGUAGES[0][0]

TIME_ZONE_UTC = 'UTC'
TIME_ZONE_ASIA_SEOUL = 'Asia/Seoul'
TIME_ZONES = [
    (TIME_ZONE_UTC, TIME_ZONE_UTC),
    (TIME_ZONE_ASIA_SEOUL, TIME_ZONE_ASIA_SEOUL),
]
TIME_ZONE = TIME_ZONES[0][0]

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/
# https://docs.sentry.io/clients/python/integrations/#integration-with-logging

LOG_FILE = os.path.join(LOGS_DIR, 'server.log')
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'semi_verbose': {
            'format': '[%(asctime)s] [%(levelname)s] %(module)s/%(funcName)s(): - %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'semi_verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'semi_verbose',
            'filename': LOG_FILE,
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10
        },
        'console_simple': {
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'simple',
        },
        'file_simple': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'simple',
            'filename': LOG_FILE,
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10
        },
    },
    'loggers': {
        'logger': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'logger_simple': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'handlers': ['console_simple', 'file_simple'],
            'propagate': False,
        },
    },
}

# Custom User
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
AUTH_USER_MODEL = 'user.User'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'EXCEPTION_HANDLER': 'app.exceptions.exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': 'app.common.PageNumberPagination',
}

SWAGGER_SETTINGS = {
    'JSON_EDITOR': True,
    'DOC_EXPANSION': 'none',
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = 'womenlink_csrftoken'
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Email Send
EMAIL_HOST = 'smtp.gmail.com'           # 메일을 호스트하는 서버
EMAIL_PORT = 587                        # gmail과의 통신하는 포트
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True                    # TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER    # 사이트와 관련한 자동응답을 받을 이메일 주소
