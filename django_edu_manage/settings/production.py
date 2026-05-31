# 生产环境配置文件。
# 这里继承 base.py 里的公共配置，只覆盖生产环境需要改变的部分。
from .base import *


# DEBUG 在生产环境默认关闭。
# True：会暴露详细错误信息，只适合开发环境。
# False：隐藏详细错误信息，生产环境必须使用。
# 生产环境建议在 .env.production 中明确写 DEBUG=False。
DEBUG = env.bool('DEBUG', default=False)


# ALLOWED_HOSTS 在生产环境必须明确配置。
# 常见值示例：
# your-domain.com
# www.your-domain.com
# api.your-domain.com
# 127.0.0.1,localhost 只适合本地或内网测试。
# * 表示允许所有主机，生产环境不建议使用。
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# ========================== 生产环境 CORS 配置 ==========================
# 生产环境只允许已知的前端域名，通过环境变量注入，不从代码中硬编码。
# 如果前端部署在 https://edu.example.com，则配置：
#   CORS_ALLOWED_ORIGINS=["https://edu.example.com"]
#
# 注意：base.py 中 CORS_ALLOW_CREDENTIALS=True，因此必须用精确的源列表，
# 不能使用通配符 * 也不能用 CORS_ALLOW_ALL_ORIGINS。
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
