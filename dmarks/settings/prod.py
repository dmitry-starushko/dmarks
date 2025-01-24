from rest_framework.permissions import IsAdminUser
from markets.enums import LogRecordKind
from .base import *

DEBUG = False

SECRET_KEY = 'QoJ?sX2.,VM=bUWhE>rzLNdUSj+y2CJ3FfZRqvhPx!exjzFaVNr<Q5LvaaavV=g>=?udMMZ+uiqMR4k3bDo59CRWDZhRhTQVXaTs'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['http://185.28.108.62/*']

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

EXT_URL = {
    'booking': 'http://web:8000/extapi/dummy1c/booking/',
    'confirmation': 'http://web:8000/extapi/dummy1c/confirmation/',
    'market-info': 'http://web:8000/extapi/dummy1c/market-info/',
    'reg-card': 'http://web:8000/extapi/dummy1c/regcard/',
    'answers': 'http://web:8000/extapi/dummy1c/answers/',
    'moderation': 'http://web:8000/extapi/dummy1c/moderation/',
}

EXT_API_PERMISSIONS = [IsAdminUser]

LOG_KINDS = frozenset({k for k in LogRecordKind})

