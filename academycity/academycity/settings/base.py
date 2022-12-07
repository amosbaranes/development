import os
from django.utils.translation import gettext_lazy as _
from braintree import Configuration, Environment

# ugettext = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # academycity/academycity
WEB_DIR = os.path.dirname(BASE_DIR)                                      # academycity
DATA_DIR = os.path.dirname(os.path.dirname(__file__))                    # academycity/academycity/setting
# print(BASE_DIR)
# print(WEB_DIR)
# print(DATA_DIR)

OBJECTS_PATH = 'objects'

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'c^58)e!54i%y#q$(@3@8nhe!hexl+j0@#%(ukx61$f-m=)bfaq'
)

# AWS_ACCESS_KEY_ID = 'AKIAZLNUPZOSSXWLSL2N'
# AWS_SECRET_ACCESS_KEY = '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'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_STORAGE_BUCKET_NAME = 'academycitystorage'
# AWS_S3_REGION_NAME = 'us-east-1'

ROOT_URLCONF = 'academycity.urls'
WSGI_APPLICATION = 'academycity.wsgi.application'
ASGI_APPLICATION = "academycity.routing.application"

# Internationalization: https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Jerusalem'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images): https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(WEB_DIR, "static")

DATA_ROOT = os.path.join(BASE_DIR, "Data")
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

# ?? djangocms-audio
# djangocms-attributes-field
# djangocms-history
# djangocms-modules
# djangocms-transfer
#
# aldryn-django
# aldryn-django-cms
# aldryn-addons
# aldryn-sso
# aldryn-snake

DJANGO_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    #
    'django.contrib.postgres',
    #
    'ckeditor',
    'ckeditor_uploader',  # < here
    #
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_file',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'channels',
    'mathfilters',
    #
    'django_elasticsearch_dsl',
    'simpy',
    'mesa',
    #
    'captcha',
]

BOOTSTRAP_APPS = [
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
]

THIRD_PARTY_APPS = [
    'rosetta',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    #
    # used pip install django-reversion
    # 'reversion',

    # 'aldryn_apphooks_config',
    # 'aldryn_boilerplates',
    # 'aldryn_categories',
    # 'aldryn_common',
    # 'aldryn_newsblog',
    # 'aldryn_people',

    # I removed this although it was asked for
    # 'aldryn_reversion',
    'parler',
    'sortedm2m',
    'taggit',
    #
    'dbbackup',  # django-dbbackup
    # 'django_extensions',

    #    'crispy_forms',
    #    'rest_framework',
]

LOCAL_APPS = [
    'academycity.apps.core',
    'academycity.apps.actions',
    'academycity.apps.images',
    'academycity.apps.ueconomics',
    'academycity.apps.users',
    'academycity.apps.courses',
    'academycity.apps.partners',
    'academycity.apps.elearning',
    'academycity.apps.blog',
    'academycity.apps.shop',
    'academycity.apps.cart',
    'academycity.apps.orders',
    'academycity.apps.payment',
    'academycity.apps.globsim',
    'academycity.apps.research',
    'academycity.apps.polls',
    'academycity.apps.chat',
    'academycity.apps.videocall',
    'academycity.apps.drbaranes',
    'academycity.apps.ugandatowns',
    'academycity.apps.webcompanies',
    'academycity.apps.openvidu',
    'academycity.apps.search',
    'academycity.apps.corporatevaluation.apps.CorporatevaluationConfig',
]

WebApps = [
    'academycity.apps.webapps.checkcashingchicago',
    'academycity.apps.webapps.education',
    'academycity.apps.webapps.portfolio',
    'academycity.apps.webapps.fabhouseafrica',
    'academycity.apps.webapps.bizland',
    'academycity.apps.webapps.apewives',
    'academycity.apps.webapps.radiusfood',
    'academycity.apps.webapps.swotclock',
    'academycity.apps.webapps.javascripttutorial',
    'academycity.apps.webapps.simba',
]

acApps = [
    'academycity.apps.acapps.acmath',
    'academycity.apps.acapps.training',
    'academycity.apps.acapps.potential',
    'academycity.apps.acapps.ms',
    'academycity.apps.acapps.avi',
    'academycity.apps.acapps.dl',
    'academycity.apps.acapps.ml',
    'academycity.apps.acapps.accounting',
    'academycity.apps.acapps.businesssim',
    'academycity.apps.acapps.liongold',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = THIRD_PARTY_APPS + LOCAL_APPS + WebApps + acApps + BOOTSTRAP_APPS + DJANGO_APPS

MIDDLEWARE = [
    # 'django_cookies_samesite.middleware.CookiesSameSite',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
    # ,
    # 'academycity.apps.core.virtualhostmiddleware.VirtualHostMiddleware'
]

DCS_SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE_FORCE_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                # 'aldryn_boilerplates.context_processors.boilerplate',
                'academycity.apps.cart.context_processors.cart',
                # 'academycity.apps.bi.context_processors.add_variable_to_context'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader'
                # 'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
            ],
        },
    },
]

# ----
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ALDRYN_BOILERPLATE_NAME='bootstrap4'

# django-allauth registraion settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional' # "mandatory"  # 'optional'   'none'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5

# 1 minute
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60  # seconds


ACCOUNT_LOGOUT_REDIRECT_URL = '/' # or '/accounts/login/'  # or to /accounts/profile/
ACCOUNT_LOGOUT_ON_GET = True

# redirects to profile page if not configured.
LOGIN_REDIRECT_URL = '/'  # or  '/accounts/email/'

SOCIALACCOUNT_QUERY_EMAIL=ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_EMAIL_REQUIRED=ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS=False

#
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'amos@DrBaranes.com'
EMAIL_HOST_PASSWORD = 'Amos122#'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# ---

CKEDITOR_UPLOAD_PATH = "uploads/"  # < here

#
LANGUAGES = (
    ## Customize this:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    #('en', ugettext('en')),
    ('en', _('English')),
    ('fr', _('French')),
    # ('es', _('Spanish')),
    ('ar', _('Arabic')),
)


CMS_LANGUAGES = {
    ## Customize this
    1: [

        {
            'code': 'en',
            'name': _('English'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
        {
            'code': 'fr',
            'name': _('French'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
        {
            'code': 'ar',
            'name': _('Arabic'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },

        # {
        #     'code': 'es',
        #     'name': _('Spanish'),
        #     'redirect_on_fallback': True,
        #     'public': True,
        #     'hide_untranslated': False,
        # },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}


PARLER_LANGUAGES = {
    1: (
        {'code': 'en',},
        {'code': 'fr',},
        {'code': 'ar', },
        # {'code': 'es', },
    ),
    'default': {
        'fallbacks': ['en'],          # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
    }
}


CMS_TEMPLATES = (
    ## Customize this
    # ('base.html', 'Home Page'),
    ('home.html', 'home'),
    ('user_home.html', 'user_home'),
    ('sidenav.html', 'Side Nave'),
    ('fullwidth.html', 'Fullwidth'),
    ('instructors.html', 'Instructors'),

    # ('syllabus.html', 'Syllabus'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    ('sidebar_both.html', 'Sidebar Both'),
)

# django-admin makemessages -l fr
# django-admin compilemessages

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

MIGRATION_MODULES = {

}

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

STATICFILES_FINDERS = [
     'django.contrib.staticfiles.finders.FileSystemFinder',
     # 'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 ]

CKEDITOR_SETTINGS = {
    'disableNativeSpellChecker': False,
    'stylesSet': [
        {
            'name': 'Page Header H1',
            'element': 'h1',
            'attributes': {
                'class': 'page-header',
                }
        },
        {
            'name': 'Page Header H2',
            'element': 'h2',
            'attributes': {
                'class': 'page-header',
                }
        },
        {
            'name': 'Page Header H3',
            'element': 'h3',
            'attributes': {
                'class': 'page-header',
                }
        },
        {
            'name': 'Page Header H4',
            'element': 'h3',
            'attributes': {
                'class': 'page-header',
                }
        },
        {
            'name': 'Code',
            'element': 'code',
        },
        {
            'name': 'Code Block',
            'element': 'pre',
            'attributes': {
                'class': 'code',
            }
        },
]
}


# Database backup
# DropBox: Token = mgDKBEyxfz8AAAAAAAAK-nu0HBxbCy9QINbwzOFKFb-PGDPN3BhVhFmYtvTpwUX-

# DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
# DROPBOX_OAUTH2_TOKEN = 'mgDKBEyxfz8AAAAAAAAK-nu0HBxbCy9QINbwzOFKFb-PGDPN3BhVhFmYtvTpwUX-'
#
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': STATIC_ROOT+'/postgres_backup/'}

#
# DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
# DBBACKUP_STORAGE_OPTIONS = {
#     'oauth2_access_token': 'mgDKBEyxfz8AAAAAAAAK-nu0HBxbCy9QINbwzOFKFb-PGDPN3BhVhFmYtvTpwUX-',
#     'root_path': os.path.join(BASE_DIR, "media")
# }
#
# DROPBOX_ROOT_PATH = os.path.join(BASE_DIR, "media")

# pip install dropbox
# pip install django-dbbackup
# pip install dropbox django-storages

CART_SESSION_ID = 'cart'
WEB_SITE_COMPANY_ID = 'WebSiteCompany'

CART_COURSES_ID = 'course_cart'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


DJANGOCMS_BOOTSTRAP4_CAROUSEL_ASPECT_RATIOS = (
    (16, 9),
    (14, 9),
    (12, 9),
    (10, 5),
    (15, 5),
    (20, 5),
    (25, 5),
)

X_FRAME_OPTIONS = 'SAMEORIGIN'   # 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

#
# https://pypi.org/project/django-recaptcha/#requirements
# https://micropyramid.medium.com/django-model-managers-and-properties-564ef668a04c?p=620b28644ef2
# https://developers.google.com/recaptcha/docs/v3
# https://www.google.com/recaptcha/admin/site/479260808/
# https://www.google.com/recaptcha/admin/site/479260808/settings
#

RECAPTCHA_PUBLIC_KEY = '6LeI8JAcAAAAAG7fUvIvZMYHCTzqh3Hte_ulUiS1'
RECAPTCHA_PRIVATE_KEY = '6LeI8JAcAAAAACKrZcgZca7Qjg4v0IRlzRqt6cYA'
RECAPTCHA_DOMAIN = 'www.recaptcha.net'
