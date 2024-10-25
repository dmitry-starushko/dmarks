from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

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