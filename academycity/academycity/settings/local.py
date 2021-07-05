from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'academycity',
        'USER': 'academycity',
        'PASSWORD': 'academycity',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

CURRENT_URL = 'local'

