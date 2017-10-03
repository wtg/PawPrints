"""
Django settings for pawprints project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from pawprints import secrets 
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["129.21.147.101"]

# Celery Settings
CELERY_BROKER_URL = secrets.RABBITMQ_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_IMPORTS = ['send_mail.tasks']

# Application definition

INSTALLED_APPS = [
    'profile.apps.ProfileConfig',
    'petitions.apps.PetitionsConfig',
    'send_mail.apps.SendMailConfig',
    'social.apps.SocialConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'channels',
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        "ROUTING": "pawprints.routing.channel_routing",
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pawprints.urls'

TEMPLATES = [
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

STATICFILES_DIRS = [STATIC_DIR, ]
WSGI_APPLICATION = 'pawprints.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secrets.DB_NAME,
        'USER': secrets.DB_USER,
        'PASSWORD': secrets.DB_PASSWORD,
        'HOST': secrets.DB_HOST,
        'PORT': secrets.DB_PORT,
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
)

# LDAP configurations
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
}
AUTH_LDAP_SERVER_URI = "ldaps://ldap.rit.edu"

AUTH_LDAP_BIND_DN = "uid=" + secrets.LDAP_USER + ",ou=People,dc=rit,dc=edu"
AUTH_LDAP_BIND_PASSWORD = secrets.LDAP_PASSWORD
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=rit,dc=edu", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Groups,dc=rit,dc=edu", ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

#Require student, prevent others
AUTH_LDAP_REQUIRE_GROUP = "cn=student,ou=Groups,dc=rit,dc=edu"
AUTH_LDAP_DENY_GROUP = "cn=staff,ou=Groups,dc=rit,dc=edu"
AUTH_LDAP_DENY_GROUP = "cn=faculty,ou=Groups,dc=rit,dc=edu"
AUTH_LDAP_DENY_GROUP = "cn=studemp,ou=Groups,dc=rit,dc=edu"

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Email settings

EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = secrets.EMAIL_PORT
EMAIL_USE_TLS = secrets.EMAIL_USE_TLS

STATIC_URL = '/static/'

LOGIN_URL = '/login/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s : %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'rotate_file_errors':{
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/error.log'),
            'formatter': 'verbose',
            'maxBytes': 90000000,
            'backupCount': 10,
            'encoding': 'utf8'
        },
        'rotate_file_info':{
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/info.log'),
            'formatter': 'verbose',
            'maxBytes': 90000000,
            'backupCount': 10,
            'encoding': 'utf8'
        },
        'slack_handler': {
            'level': 'ERROR',
            'class': 'log.slackhandler.SlackHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'pawprints': {
            'handlers': ['rotate_file_info'],
            'level': 'INFO',
            'propagate': True,
        },
        'pawprints': {
            'handlers': ['rotate_file_errors', 'slack_handler'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['rotate_file_errors', 'slack_handler'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}
