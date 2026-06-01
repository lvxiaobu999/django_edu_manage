import os
from pathlib import Path


def get_logging_config(BASE_DIR):
    """根据环境变量构建 LOGGING 配置，返回交给 settings/base.py 的 LOGGING 变量。"""

    # === 从环境变量读取配置 ===
    # LOG_LEVEL：低于此级别的日志会被丢弃（DEBUG < INFO < WARNING < ERROR）
    # 开发环境 .env.development 里默认 DEBUG，生产环境 .env.production 里默认 INFO
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # LOG_DIR：日志文件存放目录，默认项目根目录下的 logs/
    LOG_DIR = Path(os.environ.get('LOG_DIR', BASE_DIR / 'logs'))

    # LOG_BACKUP：日志保留天数，超过此天数的旧文件自动删除
    LOG_BACKUP = int(os.environ.get('LOG_BACKUP', '30'))

    # 确保日志目录存在（不存在则自动创建，已存在则跳过）
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    return {
        # version: LOGGING 配置格式版本，目前只能是 1
        'version': 1,

        # disable_existing_loggers: False 表示不禁用 Django 已有的 logger，
        # 我们只覆盖需要自定义的部分，其余保持 Django 默认行为
        'disable_existing_loggers': False,

        # ================================================================
        # formatters: 定义日志的输出格式
        # ================================================================
        'formatters': {
            # verbose：文件日志使用的详细格式
            # {asctime}         时间戳（精确到秒）
            # {levelname}       日志级别（DEBUG/INFO/WARNING/ERROR）
            # {name}            记录器名称（即 logging.getLogger(__name__) 的 __name__）
            # {request_id}      请求 ID，由 RequestIdFilter 注入 ← 生产排查的关键字段
            # {message}         日志正文
            'verbose': {
                'format': '{asctime} [{levelname}] [{name}] [req:{request_id}] {message}',
                'style': '{',           # 使用 str.format() 风格的占位符
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            # simple：控制台使用的简洁格式，去掉时间戳和模块名，方便开发时快速扫读
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },

        # ================================================================
        # filters: 日志过滤器 —— 在日志发出前对 record 做修改
        # ================================================================
        'filters': {
            # request_id 过滤器：从 thread-local 中读取当前请求的 request_id，
            # 设置到 record.request_id 上，这样 formatter 里的 {request_id} 就能取到值
            'request_id': {
                '()': 'django_edu_manage.common.logging.RequestIdFilter',
            },
        },

        # ================================================================
        # handlers: 日志处理器 —— 决定日志写到哪
        # ================================================================
        'handlers': {
            # console: 输出到 stdout（终端 / Docker 日志 / K8s 日志）
            # level=DEBUG: 控制台始终输出 DEBUG 及以上，不受 LOG_LEVEL 限制
            # 这样开发时终端能看到所有日志，生产环境 docker logs 也能看到细节
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'filters': ['request_id'],
            },

            # file: 主日志文件，写入 LOG_LEVEL 及以上级别的日志
            # DailyRotatingFileHandler 是我们自定义的 handler：
            #   - 每天生成一个文件，文件名格式 app-{日期}-{级别}.log
            #   - 例如 app-2026-06-01-INFO.log
            #   - 跨天自动切换新文件，旧文件超过 LOG_BACKUP 天自动删除
            'file': {
                'level': LOG_LEVEL,                                          # 只记录 LOG_LEVEL 及以上的日志
                'class': 'django_edu_manage.common.logging.DailyRotatingFileHandler',
                'log_dir': str(LOG_DIR),                                    # 日志目录路径
                'prefix': 'app',                                            # 文件名前缀
                'level_name': LOG_LEVEL,                                    # 文件名中的级别标识
                'backup_count': LOG_BACKUP,                                 # 保留天数
                'formatter': 'verbose',
                'filters': ['request_id'],
            },

            # error_file: 错误日志文件，只记录 ERROR 及以上级别的日志
            # 与 file handler 分开的好处：出问题时直接看 error 文件，不会被大量 INFO 干扰
            # 注意 level='ERROR' 是写死的，不受 LOG_LEVEL 影响——无论环境如何，错误必须记录
            'error_file': {
                'level': 'ERROR',
                'class': 'django_edu_manage.common.logging.DailyRotatingFileHandler',
                'log_dir': str(LOG_DIR),
                'prefix': 'app',
                'level_name': 'ERROR',                                      # 文件名固定为 ERROR
                'backup_count': LOG_BACKUP,
                'formatter': 'verbose',
                'filters': ['request_id'],
            },
        },

        # ================================================================
        # loggers: 记录器 —— 不同模块使用不同的 logger，可以各自控制级别和输出目标
        #
        # 一条日志的传递路径：
        #   logger.info(...)  →  检查 logger.level  →  handler.level  →  formatter  →  输出
        #
        # propagate: 是否向上级 logger 传递（子 logger → 父 logger → root）
        #   设为 False 是因为每个 logger 已经配置了自己的 handler，
        #   如果 propagate=True，同一条日志会被 root 重复输出一遍
        # ================================================================
        'loggers': {
            # django: Django 框架自身的运行日志（如 migrate、autoreload 等）
            # 不接入 error_file，因为框架启动时的 ERROR 通常是配置问题，不是业务错误
            'django': {
                'handlers': ['console', 'file'],
                'level': LOG_LEVEL,
                'propagate': False,
            },

            # django.request: HTTP 请求处理日志
            # Django 在处理请求时，遇到 4xx/5xx 会自动调用 logger.warning() / logger.error()
            # 所以这个 logger 接入 error_file，确保请求异常能被独立记录
            'django.request': {
                'handlers': ['console', 'file', 'error_file'],
                'level': LOG_LEVEL,
                'propagate': False,
            },

            # django.security: 安全相关事件（如 SuspiciousOperation、CSRF 校验失败等）
            # 同样接入 error_file，安全事件需要独立追踪
            'django.security': {
                'handlers': ['console', 'file', 'error_file'],
                'level': LOG_LEVEL,
                'propagate': False,
            },

            # apps: 我们自己写的业务代码
            # 在 apps/ 下任何模块里使用 logging.getLogger(__name__) 都会命中这个 logger
            # 因为 logger 名称是层级匹配的：apps.users.views → apps.users → apps
            'apps': {
                'handlers': ['console', 'file', 'error_file'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
        },

        # ================================================================
        # root: 根 logger —— 所有未被上面 logger 捕获的日志最终会到这里
        # ================================================================
        # level=WARNING 写死：第三方库（如 django-environ、corsheaders 等）的 DEBUG/INFO
        # 不需要记录，否则日志会被大量无用信息淹没。只记录 WARNING 及以上的异常信号。
        'root': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
        },
    }
