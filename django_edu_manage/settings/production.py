from .base import *


# 生产环境默认关闭调试模式；上线时应通过 .env.production 明确配置 SECRET_KEY 和 ALLOWED_HOSTS。
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
