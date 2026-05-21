import os


# 这个文件用于兼容 django_edu_manage.settings 这种导入方式。
# 如果外部没有明确指定 django_edu_manage.settings.development 或 production，
# 这里会根据 DJANGO_ENV 自动选择实际配置文件。
#
# 当前支持的 DJANGO_ENV：
# development：开发环境，默认值。
# production：生产环境。
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development').strip().lower() or 'development'


# DJANGO_ENV=production 时加载生产配置。
# 其他情况都回退到开发配置，避免拼错环境名导致项目直接不可用。
if DJANGO_ENV == 'production':
    from .production import *
else:
    from .development import *
