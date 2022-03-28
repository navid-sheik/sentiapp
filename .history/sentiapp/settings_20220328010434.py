"""
Django settings for sentiapp project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


from pathlib import Path
import os
import ssl
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v#z9t*u-h(5k)!7#=#$cy=jh1f&k)nc-cun8#jt0r2x(iy7-ek'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'crispy_forms',

 
    'django_celery_beat',
    'django_celery_results',
    'miner',
    'channels',
    'singleticker'

]

CRISPY_TEMPLATE_PACK =  'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sentiapp.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'sentiapp.wsgi.application'
ASGI_APPLICATION = "sentiapp.asgi.application"



CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#POST GRES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd8vo5d9u0dnks5', 
        'USER': 'iykgdslhfpqypi', 
        'PASSWORD': '47847c4b45175c24f5a8ba62042debbaa82c00fd761a4b8b82f9e1000c37b3ad',
        'HOST': 'ec2-52-44-209-165.compute-1.amazonaws.com', 
        'PORT': '5432',
    }
}

import dj_database_url
db_from_env  =  dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR ,'static')

MEDIA_ROOT =Path(BASE_DIR, 'media')
MEDIA_URL =  '/media/'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTH_USER_MODEL = 'mainapp.User'

CELERY_BROKER_URL  =  os.environ['REDIS_URL']
# CELERY_BROKER_URL  =  'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT  =  ['application/json']
CELERY_RESULT_SERIALIZER =  'json'
CELERY_TASK_SERIALIZER =  'json'
CELERY_TIMEZONE =  'Europe/London'
CELERY_RESULT_BACKEND = "django-db"

CELERY_WORKER_CONCURRENCY = 2   # this is the one I was actually looking for
CELERY_MAX_TASKS_PER_CHILD = 2
#celery beat setting

CELERY_BEAT_SCHEDULER =  'django_celery_beat.schedulers:DatabaseScheduler'


DATA_UPLOAD_MAX_NUMBER_FIELDS = 50000