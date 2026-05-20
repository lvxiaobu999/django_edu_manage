import os
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# 环境变量优先级：系统环境变量 > .env.*.local > .env.local > .env.development/.env.production > .env。
_settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', '')
_settings_env = _settings_module.rsplit('.', 1)[-1]
_default_env = _settings_env if _settings_env in {'development', 'production'} else 'development'
DJANGO_ENV = os.environ.get('DJANGO_ENV', _default_env).strip().lower() or _default_env
_original_environ = os.environ.copy()
environ.Env.read_env(BASE_DIR / '.env')
environ.Env.read_env(BASE_DIR / f'.env.{DJANGO_ENV}', overwrite=True)
environ.Env.read_env(BASE_DIR / '.env.local', overwrite=True)
environ.Env.read_env(BASE_DIR / f'.env.{DJANGO_ENV}.local', overwrite=True)
os.environ.update(_original_environ)


SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me-for-development')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_app.apps.DjangoAppConfig',
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

ROOT_URLCONF = 'django_edu_manage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_edu_manage.wsgi.application'


# 使用 DATABASE_URL 统一管理 PostgreSQL 等外部数据库连接。
# 示例：postgres://django_user:django_password@localhost:5432/django_edu_manage
DATABASE_URL = env('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES = {
        'default': env.db('DATABASE_URL')
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
