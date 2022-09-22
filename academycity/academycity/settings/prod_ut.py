from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SITE_ID = 3

ADMINS = (
    ('Amos Baranes', 'ac@drbaranes.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}

MEDIA_ROOT = '/usr/src/app/academycitymedia/'  # for nginx
STATIC_ROOT = '/usr/src/app/academycitystatic/'  # for nginx

CURRENT_URL = 'prod_ut'

REDIS_HOST = 'redis'
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
            "hosts": [('redis', 6379)],
        },
    },
}

DOMAIN = 'https://academycity.org'
