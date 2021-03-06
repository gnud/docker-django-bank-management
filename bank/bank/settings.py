"""
Django settings for bank project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import logging.config
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vdc-3!re1ddl+ku6sa3tj&gqxo^u7jp$-apb%5a-r31e1xc^pn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = ['localhost', '0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'banking',

    # Social integration
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bank.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'banking', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Social integration
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'bank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR'),
        'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
#
STATIC_URL = '/static/'
#
# Collect static won't work if you haven't configured this
# django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set
#  the STATIC_ROOT setting to a filesystem path.
STATIC_ROOT = 'static/'

# Indicate that we're being executed by uWSGI
# This settings is used in urls.py to serve the static from within uWSGI
IS_WSGI = bool(os.environ.get('IS_WSGI', False))

# Setup support for proxy headers
# https://design.canonical.com/2015/08/django-behind-a-proxy-fixing-absolute-urls
# http://stackoverflow.com/questions/19669376/django-rest-framework-absolute-urls-with-nginx-always-return-127-0-0-1
# http://stackoverflow.com/questions/26435272/how-to-use-django-sslify-to-force-https-on-my-djangonginxgunicorn-web-app-and
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')


# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'debug').upper()


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        # 'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'db': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'db.log'),
            'formatter': 'main_formatter',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'info.log'),
            'formatter': 'main_formatter',
        },
        'errors': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'errors.log'),
            'formatter': 'main_formatter',
        },
        'other': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'other.log'),
            'formatter': 'main_formatter',
        },
        'requests': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'requests.log'),
            'formatter': 'main_formatter',
        },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'main_formatter',
        },

        # 'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['requests'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # default for all undefined Python modules
        '': {
            'level': 'DEBUG',
            'handlers': ['other'],
        },
        # Our application code
        'app': {
            'level': LOGLEVEL,
            'handlers': ['file'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        # Prevent noisy modules from logging to Sentry
        'noisy_module': {
            'level': 'ERROR',
            'handlers': ['errors'],
            'propagate': False,
        },
        'django.contrib.auth.backends.ModelBackend': {
            'level': 'DEBUG',
            'handlers': ['db'],
        }
        # Default runserver request logging
        # 'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    }
})


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
)

# Google configuration
# Create new Google Web application
# https://console.cloud.google.com/apis/credentials/oauthclient/
# Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ' {MY KEY GOOGLE}.apps.googleusercontent.com '
# Client secret
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'MYSECRET'
GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'token_expiry': None, 'access_type': 'offline'}

LOGIN_REDIRECT_URL = '/admin/'
