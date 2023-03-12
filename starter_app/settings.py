# flake8: noqa
"""
Django settings for starter_app project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/

Sections:

- ## Env ##
- ## Django basic ##
- ## Customized settings ##
- ## Application definition ##
- ## Database ##
- ## Password validation ##
- ## Logging ##
- ## Internationalization ##
- ## Static files (CSS, JavaScript, Images) ##
"""

import logging
from pathlib import Path
from .utils.settings import EnvBase


## Env ##

class Env(EnvBase):
    DEBUG = (bool, True)
    DB_URL = (str, '')
    FAKE_HEADER_AUTH = (bool, False)
    LOG_LEVEL_APP = (str, 'INFO')
    LOG_LEVEL_DB = (str, 'INFO')

    class Meta:
        env_file = 'starter_app.env'


## Django basic ##

APP_DIR = Path(__file__).resolve().parent
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = APP_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%rop%my9(&2%9848_p(f)v)5rvv-+rt2!c!8zjzks8fxpurkhr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Env.DEBUG
FAKE_HEADER_AUTH = Env.FAKE_HEADER_AUTH

ALLOWED_HOSTS = ['*']

ADMIN_TITLE = 'starter_app Admin'


## Customized settings ##

# Application environment name, examples: 'prod', 'uat', 'dev', 'local', 'prod.us', 'uat.hk'
APP_ENV = None

# Sentry settings
SENTRY_DSN = None

# REDIS_URL = 'redis://[:password]@localhost:6379/0'
REDIS_URL = None


## Application definition ##

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'starter_app.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'starter_app.lib.middlewares.ResponseMiddleware',
]

ROOT_URLCONF = 'starter_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'starter_app.lib.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'starter_app.wsgi.application'


## Database ##
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES['default'].update(Env._env.db('DB_URL'))

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# # Used with db_router module
# DATABASE_ROUTERS = ['starter_app.db_router.DefaultRouter']


## Password validation ##
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


## Logging ##

# LOG_FORMAT = '[%(name)s] %(levelname)s %(message)s t=%(asctime)s p=%(pathname)s:%(lineno)d'
LOG_FORMAT = '%(asctime)s  %(levelname)s  %(name)-10s  %(message)s'

# LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'starter_app': {
            'handlers': ['stream'],
            'level': getattr(logging, Env.LOG_LEVEL_APP),
        },
        # Disable unnecessary 4xx log
        'django.request': {
            'level': 'ERROR',
            'handlers': ['stream'],
            'propagate': 0,
        },
        'django.db': {
            'level': getattr(logging, Env.LOG_LEVEL_DB),
            'handlers': ['stream'],
            'propagate': 0,
        },

        # other third party libs
        'requests': {
            'level': 'WARNING',
            'handlers': ['stream'],
            'propagate': 0,
        },
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'common',
        },
    },
    'formatters': {
        'common': {
            'format': LOG_FORMAT,
            'datefmt': LOG_DATE_FORMAT,
        },
    },
}


## Internationalization ##
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


## Static files (CSS, JavaScript, Images) ##
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Will be used for django_static_collector
STATIC_ROOT = 'static'

# # Determine the process of static collecting
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static_src'),
# ]
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
# ]
