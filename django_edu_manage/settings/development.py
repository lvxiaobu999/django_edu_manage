# 开发环境配置文件。
# 这里继承 base.py 里的公共配置，只覆盖开发环境需要改变的部分。
from .base import *


# DEBUG 在开发环境默认打开。
# True：浏览器会展示详细错误页面，方便调试。
# False：隐藏详细错误，生产环境必须使用。
# 如果 .env.development 或 .env.development.local 里配置了 DEBUG，则以环境文件为准。
DEBUG = env.bool('DEBUG', default=True)


# 开发环境默认允许本机访问。
# 可选值示例：
# 127.0.0.1：本机 IPv4 回环地址。
# localhost：本机主机名。
# 0.0.0.0：通常用于 runserver 监听所有网卡时配合访问。
# example.com：正式域名，通常在生产环境配置。
# *：允许所有主机，开发调试可临时用，生产环境不建议使用。
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
