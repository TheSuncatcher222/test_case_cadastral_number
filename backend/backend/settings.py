from datetime import timedelta
import os

from corsheaders.defaults import default_headers

from backend.app_data import (
    BASE_DIR,
    DATABASE_SQLITE, DATABASE_POSTGRESQL,
    SECRET_KEY,
)


"""App settings."""


DEBUG = False


"""Celery settings."""


CELERY_BROKER_URL = 'redis://cadastral_redis:6379/0'

CELERY_RESULT_BACKEND = 'redis://cadastral_redis:6379/0'

CELERY_TASK_TRACK_STARTED = True

# INFO: установлено значение 5 минут, так как максимальный пинг сервера
#       составляет 60 секунд, в каждой асинхронной задаче будет запрос
#       на пакетное изменение (bulk_update) не более 5 объектов модели.
# INFO: значение задается в секундах
# INFO: сейчас на сервере указан пинг не более 10 секунд.
CELERY_TASK_TIME_LIMIT = 10

CELERY_TIMEZONE = 'Europe/Moscow'

CELERY_BEAT_SCHEDULE = {
    'validate_cadastral_numbers': {
        'task': 'cadastral.tasks.validate_cadastral_numbers',
        'schedule': timedelta(seconds=CELERY_TASK_TIME_LIMIT),
    },
}

# INFO: показывает, сколько объектов кадастровых номеров
#       должны обрабатываться в одной асинхронной группе.
CHUNK_CELERY: int = 5


"""Django settings."""


DATABASES = DATABASE_SQLITE if DEBUG else DATABASE_POSTGRESQL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS_DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_THIRD_PARTY = [
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'django_celery_beat',
]

INSTALLED_APPS_LOCAL = [
    'api',
    'cadastral',
]

INSTALLED_APPS = INSTALLED_APPS_DJANGO + INSTALLED_APPS_THIRD_PARTY + INSTALLED_APPS_LOCAL

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

ROOT_URLCONF = 'backend.urls'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Cadastral Number Test Case',
    'DESCRIPTION': 'Test case for Antipoff IT',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r'/api/',
}

WSGI_APPLICATION = 'backend.wsgi.application'


"""Static files settings."""


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = 'static/'

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


"""Regional settings."""


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


"""Security settings."""


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

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    *default_headers,
    "access-control-allow-credentials",
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8001',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.v1.middlewares.RequestLoggingMiddleware',
]

SECRET_KEY = SECRET_KEY
