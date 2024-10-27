from .base import *

DEBUG = False

SECRET_KEY = 'QoJ?sX2.,VM=bUWhE>rzLNdUSj+y2CJ3FfZRqvhPx!exjzFaVNr<Q5LvaaavV=g>=?udMMZ+uiqMR4k3bDo59CRWDZhRhTQVXaTs'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['http://192.168.0.199/*']

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