import os
import re
from pathlib import Path
from markets.enums import LogRecordKind

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markets.apps.MarketsConfig',
    'extapi.apps.ExtapiConfig',
    'renter.apps.RenterConfig',
    'qr_code',
    'pgtrigger',
    'easy_thumbnails',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'markets.processors.processors.parameters_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'dmarks.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '10000/day'
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DMarks API',
    'DESCRIPTION': 'API сайта «Рынки Донбасса - Интерактивные карты»',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "PREPROCESSING_HOOKS": ["extapi.openapi.preprocessing_filter_spec"],
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = "markets.DmUser"

LOGIN_REDIRECT_URL = 'renter:renter'

LOGIN_URL = 'renter:login'

LOGOUT_URL = 'renter:logout'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEF_MK_IMG = 'markets/def-mk-img.webp'

USE_THOUSAND_SEPARATOR = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DISP_RE = re.compile('[^а-яА-ЯёЁ0-9.,«»()\\-]+')

REDIS_HOST = os.environ.get('REDIS_HOST')

REDIS_PORT = os.environ.get('REDIS_PORT')

REDIS_DB = os.environ.get('REDIS_DB')

SCHEME_EXPIRE_SECONDS = 600

FAIL_EXPIRE_SECONDS = 600

ASGI_APPLICATION = 'dmarks.asgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        }
    }
}

LOG_KINDS = frozenset()

LOG_TTL_DAYS_DEFAULT = 100

LOG_TTL_DAYS = {
    LogRecordKind.INFO: LOG_TTL_DAYS_DEFAULT,
    LogRecordKind.WARNING: LOG_TTL_DAYS_DEFAULT,
    LogRecordKind.ERROR: LOG_TTL_DAYS_DEFAULT,
    LogRecordKind.FATAL: LOG_TTL_DAYS_DEFAULT,
}

USE_1C_API = False

AUTH_1C_API = ''

URLS_1C_API = {
    'booking': 'http://localhost:8000/extapi/dummy1c/booking/',
    'confirmation': 'http://localhost:8000/extapi/dummy1c/confirmation/',
    'reg-card': 'http://localhost:8000/extapi/dummy1c/regcard/',
    'answers': 'http://localhost:8000/extapi/dummy1c/answers/',
    'market-info': 'http://localhost:8000/extapi/dummy1c/market-info/',
    'moderation': 'http://localhost:8000/extapi/dummy1c/moderation/',
    'check-results': 'http://localhost:8000/extapi/dummy1c/check/',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.gprd-dnr.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'maps.mail@gprd-dnr.ru'
EMAIL_HOST_PASSWORD = '7948yXS2Gp'
EMAIL_TO = ['dmitry.starushko@gmail.com']
