from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 修改这里，加上 apps. 前缀
    name = 'apps.users'
    verbose_name = '用户管理'