from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'academycity',
        'USER': 'academycity',
        'PASSWORD': 'academycity',
        'HOST': 'localhost',
        'PORT': 5432
    },
    'academycity': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'academycity',
        'USER': 'academycity',
        'PASSWORD': 'academycity',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

CURRENT_URL = 'dev'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


# Braintree settings
# https://sandbox.braintreegateway.com/merchants/9q6qtj5psh68msrf/home
BRAINTREE_MERCHANT_ID = '9q6qtj5psh68msrf'  # Merchant ID
BRAINTREE_PUBLIC_KEY = '22hj2kpq45d7jd6s'   # Public Key
BRAINTREE_PRIVATE_KEY = '09c55c429913db7bb2de953080ffd9e7'  # Private key

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            "capacity": 1500,  # default 100
            "expiry": 10,  # default 60
        },
    },
}

DOMAIN = 'http://127.0.0.1:8000'


ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}
