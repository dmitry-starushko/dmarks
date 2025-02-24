from rest_framework.permissions import IsAdminUser
from .base import *

DEBUG = False

SECRET_KEY = 'QoJ?sX2.,VM=bUWhE>rzLNdUSj+y2CJ3FfZRqvhPx!exjzFaVNr<Q5LvaaavV=g>=?udMMZ+uiqMR4k3bDo59CRWDZhRhTQVXaTs'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://maps.donmarkets.ru/*']

ADMINS = [
    ('Dmitry', 'dmitry@gmail.com'),
    ('Sergey', 'sergey@gmail.com')
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

CELERY_BROKER_URL = f'pyamqp://guest@rabbit'

TELEBOT_ID = os.environ.get('TELEBOT')

AUTH_1C_API = 'Basic UkQzRDoxMjM0NQ=='
URLS_1C_API = {
    'booking': 'http://192.168.90.15/Arenda_Test/hs/reserve/{user}/',
    'confirmation': 'http://192.168.90.15/Arenda_Test/hs/Ver/',
    'reg-card': 'http://192.168.90.15/Arenda_Test/hs/register-card/{user}/',
    'answers': 'http://192.168.90.15/Arenda_Test/hs/user-answers/{user}/',
    'moderation': 'http://192.168.90.15/Arenda_Test/hs/moderate-card/{user}/',
    'market-info': 'http://192.168.90.15/Arenda_Test/hs/market-details/{market}/',
    'check-results': 'http://192.168.90.15/Arenda_Test/hs/check-results/',
}

EXT_API_PERMISSIONS = [IsAdminUser]

LOG_KINDS = frozenset({k for k in LogRecordKind})

OG_HOST_URL = 'https://maps.donmarkets.ru'
