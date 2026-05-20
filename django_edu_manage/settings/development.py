from .base import *


# 开发环境默认打开调试模式；如果 .env.development 设置了 DEBUG，则以文件配置为准。
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
