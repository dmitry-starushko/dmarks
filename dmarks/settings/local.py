from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-%tt)nxtq^#o5686r*!_w337w&(nm9bk=44re77*36dvfo_q6+4'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGBASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSW'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': int(os.environ.get('PGPORT')),
    }
}