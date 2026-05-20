from .base import *

# 加载开发环境变量
env.read_env(BASE_DIR / '.env.development')

# 开发环境特有配置覆盖
DEBUG = env.bool('DEBUG', default=True)

# 一键解析数据库 URL
DATABASES = {
    'default': env.db('DATABASE_URL')
}

CORS_ALLOW_ALL_ORIGINS = True  # 本地开发允许跨域