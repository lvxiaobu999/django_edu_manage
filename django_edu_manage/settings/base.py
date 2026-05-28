import os
from pathlib import Path

import environ


# BASE_DIR 表示项目根目录，也就是 manage.py 所在目录。
# 这里从当前文件 settings/base.py 往上找三层：
# base.py -> settings/ -> django_edu_manage/ -> 项目根目录。
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# django-environ 的 Env 对象负责读取和转换环境变量。
# 这里先声明两个变量的类型和默认值：
# DEBUG：布尔值，可写 True/False、1/0、yes/no、on/off 等。
# ALLOWED_HOSTS：列表，环境变量里通常写成 127.0.0.1,localhost,example.com。
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)


# DJANGO_ENV 表示当前运行环境。
# 可选值当前约定为：
# development：开发环境，默认值。
# production：生产环境。
#
# 这里额外读取 DJANGO_SETTINGS_MODULE，是为了兼容 Django 原生命令：
# uv run python manage.py check --settings=django_edu_manage.settings.production
_settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', '')
_settings_env = _settings_module.rsplit('.', 1)[-1]
_default_env = _settings_env if _settings_env in {'development', 'production'} else 'development'
DJANGO_ENV = os.environ.get('DJANGO_ENV', _default_env).strip().lower() or _default_env


# 环境变量加载顺序，优先级从低到高：
# 1. .env                         通用默认配置，可以提交到 Git。
# 2. .env.development/production  某个环境的默认配置，可以提交到 Git。
# 3. .env.local                   本机通用覆盖配置，不提交到 Git。
# 4. .env.development.local       本机开发环境覆盖配置，不提交到 Git。
# 5. 系统环境变量                 最高优先级，适合服务器、CI/CD、容器平台注入。
#
# read_env(..., overwrite=True) 表示后读取的文件可以覆盖前面文件里的值。
# 最后 os.environ.update(_original_environ) 是为了保证系统环境变量优先级最高。
_original_environ = os.environ.copy()
environ.Env.read_env(BASE_DIR / '.env')
environ.Env.read_env(BASE_DIR / f'.env.{DJANGO_ENV}', overwrite=True)
environ.Env.read_env(BASE_DIR / '.env.local', overwrite=True)
environ.Env.read_env(BASE_DIR / f'.env.{DJANGO_ENV}.local', overwrite=True)
os.environ.update(_original_environ)


# SECRET_KEY 是 Django 用来做签名和安全校验的密钥。
# 用途包括 session、csrf token、密码重置链接等签名。
# 生产环境必须设置一个足够随机且保密的值，不要使用默认值。
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me-for-development')


# DEBUG 控制调试模式。
# True：开发环境常用，错误页面会显示详细堆栈。
# False：生产环境必须使用，避免泄露代码路径、环境变量等敏感信息。
DEBUG = env.bool('DEBUG')


# ALLOWED_HOSTS 表示允许访问当前 Django 服务的主机名。
# DEBUG=False 时必须配置，否则 Django 会拒绝请求。
# 常见值：
# 127.0.0.1,localhost
# example.com,www.example.com
# * 表示允许所有主机，生产环境不建议使用。
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# INSTALLED_APPS 表示启用哪些 Django 应用。
# django.contrib.* 是 Django 内置应用：
# admin：后台管理。
# auth：用户、用户组、权限。
# contenttypes：内容类型框架，权限系统等会用到。
# sessions：session 支持。
# messages：一次性消息提示。
# staticfiles：静态文件管理。
# django_app.apps.DjangoAppConfig 是本项目自己的应用。
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_app.apps.DjangoAppConfig',
    'apps.users.apps.UsersConfig',
    'apps.classes.apps.ClassesConfig',
    'apps.user_profile.apps.UserProfileConfig',
    'apps.research_group.apps.ResearchGroupConfig',
]


# MIDDLEWARE 是请求进入视图前、响应返回浏览器前会依次执行的中间件。
# 顺序很重要，通常不要随意调整 Django 默认中间件顺序。
# SecurityMiddleware：提供基础安全响应头和 HTTPS 相关能力。
# SessionMiddleware：启用 request.session。
# CommonMiddleware：处理 APPEND_SLASH 等通用行为。
# CsrfViewMiddleware：提供 CSRF 防护。
# AuthenticationMiddleware：把当前用户挂到 request.user。
# MessageMiddleware：支持 django.contrib.messages。
# XFrameOptionsMiddleware：防止页面被 iframe 嵌入引发点击劫持。
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ROOT_URLCONF 指定根路由模块。
# Django 会从 django_edu_manage/urls.py 里读取 urlpatterns。
ROOT_URLCONF = 'django_edu_manage.urls'


# TEMPLATES 配置模板系统。
# BACKEND：模板引擎，当前使用 Django 自带模板引擎。
# DIRS：项目级模板目录，这里是项目根目录下的 templates/。
# APP_DIRS=True：允许 Django 自动查找各 app/templates/ 目录。
# context_processors：模板上下文处理器，会给模板自动注入常用变量。
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


# WSGI_APPLICATION 指定 WSGI 应用入口。
# 传统同步部署方式会用它，例如 gunicorn、uWSGI、mod_wsgi。
WSGI_APPLICATION = 'django_edu_manage.wsgi.application'


# DATABASE_URL 用于统一描述数据库连接。
# PostgreSQL 示例：
# postgres://django_user:django_password@localhost:5432/django_edu_manage
# SQLite 示例：
# sqlite:///db.sqlite3
# MySQL 示例，前提是安装对应驱动：
# mysql://user:password@localhost:3306/db_name
#
# 当前策略：
# 配置了 DATABASE_URL，就交给 django-environ 解析。
# 没有配置 DATABASE_URL，就回退到本地 SQLite，方便刚拉项目时直接运行。
DATABASE_URL = env('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES = {
        'default': env.db('DATABASE_URL')
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db_v2.sqlite3',
        }
    }


# AUTH_PASSWORD_VALIDATORS 是 Django 内置密码强度校验器。
# UserAttributeSimilarityValidator：密码不能和用户名、邮箱等太相似。
# MinimumLengthValidator：密码最小长度校验，默认至少 8 位。
# CommonPasswordValidator：禁止使用常见弱密码。
# NumericPasswordValidator：禁止纯数字密码。
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


# LANGUAGE_CODE 表示默认语言。
# 常见值：
# en-us：美式英语。
# zh-hans：简体中文。
# zh-hant：繁体中文。
# ja：日语。
# ko：韩语。
LANGUAGE_CODE = 'en-us'


# TIME_ZONE 表示项目默认时区。
# 当前值 UTC 表示协调世界时，常用于服务器和数据库统一存储。
# 中国大陆常用：Asia/Shanghai。
# 其他常见值：Asia/Tokyo、Europe/London、America/New_York。
# 完整可选值来自 IANA 时区数据库，不是随便写的字符串。
TIME_ZONE = 'UTC'


# USE_I18N 控制是否启用国际化翻译系统。
# True：启用 Django 的翻译、语言格式化等能力。
# False：关闭国际化，稍微减少一点额外处理。
USE_I18N = True


# USE_TZ 控制 Django 是否使用带时区的时间。
# True：推荐值，数据库内部通常按 UTC 存储，展示时再按 TIME_ZONE 转换。
# False：使用朴素 datetime，容易在跨时区或部署后产生时间问题。
USE_TZ = True


# STATIC_URL 是静态文件访问 URL 前缀。
# 当前值 static/ 表示静态资源路径类似 /static/app.css。
# 生产环境通常还会配置 STATIC_ROOT，用 collectstatic 收集静态文件。
STATIC_URL = 'static/'

AUTH_USER_MODEL = 'users.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
