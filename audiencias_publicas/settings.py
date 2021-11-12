# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from decouple import config, Csv
from dj_database_url import parse as db_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       cast=Csv(lambda x: x.strip().strip(',').strip()),
                       default='*')

# Application definition

INSTALLED_APPS = (
    'apps.core',
    'apps.accounts',
    'apps.notification',
    'apps.reports',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'constance',
    'constance.backends.database',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
    'corsheaders',
    'macros',
    'drf_yasg',
    'django_celery_beat',
    'django_celery_results',

    'djangobower',
    'compressor',
    'compressor_toolkit',
    'channels',
    'channels_presence',
    'django_js_reverse',
)

AUTH_USER_MODEL = 'accounts.User'

SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS'
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'apps.core.permissions.ApiKeyPermission',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

CAMARA_LOGIN = config('CAMARA_LOGIN', default=False, cast=bool)
QUESTION_MIN_UPVOTES = config('QUESTION_MIN_UPVOTES', default=3, cast=int)
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
OLARK_ID = config('OLARK_ID', default='')
WEBSERVICE_URL = config('WEBSERVICE_URL', default='')
RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'apps.accounts.middlewares.AudienciasRemoteUser',
)

ROOT_URLCONF = 'audiencias_publicas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'constance.context_processors.config',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'apps.core.processors.analytics',
            ],
            'libraries' : {
                'staticfiles': 'django.templatetags.static', 
            }
        },
    },
]

# WSGI_APPLICATION = 'audiencias_publicas.wsgi.application'
# Channels
ASGI_APPLICATION = 'audiencias_publicas.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + config('DATABASE_ENGINE',
                                                 default='sqlite3'),
        'NAME': config('DATABASE_NAME', default='db.sqlite3'),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}

# Internationalization
LANGUAGES = (
    ('en', 'English'),
    ('pt-br', 'Brazilian Portuguese'),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = config('STATIC_URL', default='/static/')

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'templates/components/edem-navigation/static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
]

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')

BOWER_INSTALLED_APPS = [
    'jquery#~2.2.0',
    'foundation-sites#~6.2.4',
    'mixitup#~2.1.11',
    'https://github.com/labhackercd/fontastic-labhacker.git',
    'https://github.com/joewalnes/reconnecting-websocket.git',
    'jquery-ui#~1.12.1',
]

BOWER_PATH = os.path.join(BASE_DIR, 'node_modules/.bin/bower')
BROWSERIFY = os.path.join(BASE_DIR, 'node_modules/.bin/browserify')

COMPRESS_NODE_MODULES = os.path.join(BASE_DIR, 'node_modules')
COMPRESS_NODE_SASS_BIN = os.path.join(BASE_DIR, 'node_modules/.bin/node-sass')
COMPRESS_POSTCSS_BIN = os.path.join(BASE_DIR, 'node_modules/.bin/postcss')

COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
    ('text/es6', BROWSERIFY + ' {infile} -t babelify --outfile {outfile}')
]

COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')
COMPRESS_OFFLINE = config('COMPRESS_OFFLINE', default=False)

LIBSASS_SOURCEMAPS = 'DEBUG'

if DEBUG:
    COMPRESS_SCSS_COMPILER_CMD = '{node_sass_bin}' \
                                 ' --source-map true' \
                                 ' --source-map-embed true' \
                                 ' --source-map-contents true' \
                                 ' --output-style expanded' \
                                 ' {paths} "{infile}" "{outfile}"' \
                                 ' &&' \
                                 ' {postcss_bin}' \
                                 ' --use "{node_modules}/autoprefixer"' \
                                 ' --autoprefixer.browsers' \
                                 ' "{autoprefixer_browsers}"' \
                                 ' -r "{outfile}"'

# Authentication stuffs
URL_PREFIX = config('URL_PREFIX', default='')
FORCE_SCRIPT_NAME = config('FORCE_SCRIPT_NAME', default='')
LOGIN_URL = config('LOGIN_URL', default='/login/')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', default='/')
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', default='/')

SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', default='sessionid')
SESSION_COOKIE_PATH = config('SESSION_COOKIE_PATH', default='/')

# Social auth
if config('ENABLE_REMOTE_USER', default=0, cast=bool):
    AUTHENTICATION_BACKENDS = (
        'apps.accounts.backends.AudienciasAuthBackend',
    )
else:
    AUTHENTICATION_BACKENDS = (
        'rules.permissions.ObjectPermissionBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

# Email configuration

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(config('REDIS_SERVER', default='localhost'), 6379)],
        },
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'chat': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}

NOTIFICATION_EMAIL_LIST = config(
    'NOTIFICATION_EMAIL_LIST',
    cast=Csv(lambda x: x.strip().strip(',').strip()),
    default=''
)

# EDITABLE SETTINGS
CONSTANCE_CONFIG = {
    'SITE_NAME': ('Câmara dos Deputados', 'Nome do site', str),
    'HOME_DESCRIPTION': ('Acompanhe ao vivo e participe enviando perguntas aos '
                         'deputados!', 'Descrição que acompanha a logo', str),
    'QUESTIONS_DESCRIPTION': ('Faça sua pergunta ou apoie outra já feita. As '
                              'perguntas mais votadas serão encaminhadas à '
                              'Mesa para serem respondidas.', 'Descrição da '
                              'aba de perguntas', str),
    'ROOM_OBJECT': ('Pauta', 'Título do objeto da reunião', str),
    'WORDS_BLACK_LIST': (
        'merda, cu, cuzao, cuzona, cusao, cusona, bunda, fodido, fodida, foda, foder, '
        'fodedor, fudido, fudida, fuder, chupa, chupada, chupador, chupadora, '
        'boquete, boqueteira, boquetera, boketeira, boketera, xupa, xupada, xupador, '
        'xupadora, pauduro, pauzudo, xoxota, chochota, buceta, boceta, busseta, '
        'bosseta, cacete, cassete, caceta, kacete, kassete, caralho, karalho, '
        'caraleo, pinto, pica, rola, roludo, gozado, gozada, goso, gosa, gosado, '
        'gosado, puta, puto, putinho, putinha, putona, putana, putaria, grelo, '
        'grelinho, filhodaputa, filhosdaputa, puta, fdps, siririca, punheta, trepar, '
        'trepada, trepadeira, caralho, caralhu, karalho, karalhu, tomarnocu, '
        'tomanocu, vadia, bosta, quenga, rabo, bolsa, cuzinho, piroca, pqp, puta que '
        'pariu, porra, carai, cú, viado, fdp, vtnc, corno, bicha, bixa, viado, viadinho, '
        'pederasta, filho da puta, bundao, bundão, filho de uma egua, '
        'filho de uma égua, achacador, achacadora, achacadores, achacar, babaca, '
        'bucetas, cagar, cagaram, cambada, caráleo, corja, cornão, covarde, covardes, '
        'cretino, cus, cús, cusão, cuzão, cuzinho, cuzona, danar, desgraça, drosoba, '
        'enrabar, escória, escroto, escrotas, escrotos, fodão, fodona, fudendo, '
        'fuder, idiota, imundo, imundos, ku, kú, lascar, merdas, patifaria, pilantra, '
        'pilantragem, pilantras, poha, porcaria, putas, putos, sacanagem, safadeza, '
        'safado, safados, salafrário, salafrários, vagabundagem, vagabundo, '
        'vagabundos, veadinho, veadinhos',
        'Lista de palavras e termos censurados. Devem ser separadas por '
        'vírgula.',
        str
    ),
    'WELCOME_MESSAGE': (
        '', 'Mensagem de boas vindas quando iniciar a trasmissão',  str),
    'WELCOME_MESSAGE_USER_ID': (
        0, 'Id do usuário que irá mandar as mensagens de boas-vindas', int),
    'WELCOME_VIDEO': (
        '',
        'Vídeo introdutório que irá aparecer assim que a sala for criada',
        str
    ),
    'WELCOME_VIDEO_TITLE': (
        'Saiba mais',
        'Título do vídeo introdutório que irá aparecer assim que a sala '
        'for criada',
        str
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Geral': ('SITE_NAME', 'WORDS_BLACK_LIST'),
    'Página inicial': ('HOME_DESCRIPTION', ),
    'Página de sala': ('QUESTIONS_DESCRIPTION', 'ROOM_OBJECT'),
    'Mensagens': (
        'WELCOME_MESSAGE', 'WELCOME_MESSAGE_USER_ID', 'WELCOME_VIDEO',
        'WELCOME_VIDEO_TITLE')
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

# Celery
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_ENABLE_UTC = False