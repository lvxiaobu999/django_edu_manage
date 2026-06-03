from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth'
    # label 必须指定，因为 django.contrib.auth 已经占用了 'auth'
    label = 'app_auth'
    verbose_name = '认证模块'
