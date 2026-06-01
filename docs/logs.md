# 日志配置

日志系统根据环境变量动态配置，文件名包含日期和日志级别，便于按天归档和检索。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `LOG_LEVEL` | `INFO` | 日志级别（`DEBUG` / `INFO` / `WARNING` / `ERROR`） |
| `LOG_DIR` | `BASE_DIR/logs/` | 日志文件输出目录 |
| `LOG_BACKUP` | `30` | 日志保留天数，超期自动删除 |

各环境 `.env` 文件中已有预设值：
- `.env.development` → `LOG_LEVEL=DEBUG`
- `.env.production` → `LOG_LEVEL=INFO`

## 日志输出

### 控制台（console）

所有环境均输出到 stdout，格式简洁：

```
INFO 用户登录成功
ERROR 数据库连接失败: connection refused
```

Docker / K8s 部署时日志通过 stdout 被容器运行时收集，无需额外配置。

### 文件日志

日志写入 `logs/` 目录，每天生成新文件，文件名格式为 `{prefix}-{date}-{level}.log`：

```
logs/
├── app-2025-06-01-INFO.log     # 6月1日 INFO 及以上日志
├── app-2025-06-01-ERROR.log    # 6月1日 ERROR 日志
├── app-2025-06-02-INFO.log     # 跨天后自动切换新文件
├── app-2025-06-02-ERROR.log
└── app-2025-05-01-INFO.log     # 30天前的文件（会被自动清理）
```

| 文件模式 | 级别 | 说明 |
|----------|------|------|
| `app-{date}-{LOG_LEVEL}.log` | `LOG_LEVEL` 以上 | 全量应用日志 |
| `app-{date}-ERROR.log` | `ERROR` 以上 | 错误日志（告警、排障） |

文件日志格式（verbose），便于 `grep` 和日志平台解析：

```
2025-06-01 12:00:00 [INFO] [apps.users.views] [req:abc-123-def] 用户 admin 登录成功
2025-06-01 12:01:05 [ERROR] [django.request] [req:def-456-ghi] 500 Internal Server Error: /api/users/
```

字段说明：
- `2025-06-01 12:00:00` — 时间戳
- `[INFO]` — 日志级别
- `[apps.users.views]` — 记录器名称（模块路径）
- `[req:abc-123]` — 请求 ID（与 API 响应 `meta.requestId` 一致）
- `用户 admin 登录成功` — 日志消息

## 日志分类

| Logger | 覆盖范围 | handler |
|--------|----------|---------|
| `django` | Django 框架运行日志 | console + file |
| `django.request` | HTTP 请求日志（400/500 自动记录） | console + file + error_file |
| `django.security` | 安全事件（SuspiciousOperation 等） | console + file + error_file |
| `apps` | 业务代码（`apps.*` 下模块） | console + file + error_file |
| root | 兜底，捕获所有未被子 logger 处理的日志 | console + file |

## 在代码中使用

```python
import logging

logger = logging.getLogger(__name__)


class LoginView(APIView):
    def post(self, request):
        logger.info('用户登录请求: username=%s', username)

        user = authenticate(request, username=username, password=password)
        if user is None:
            logger.warning('登录失败: username=%s, 密码错误', username)
            return fail(message='用户名或密码错误')

        logger.info('用户登录成功: user_id=%s, role=%s', user.id, user.role)
        return ok(data=UserSerializer(user).data)
```

### requestId 追踪

得益于 `RequestIdMiddleware` 和 `RequestIdFilter`，每条日志自动包含当前请求的 `requestId`，无需手动传入。前端报错时提供 `meta.requestId`，后端通过它 grep 日志即可快速定位：

```bash
# 根据前端反馈的 requestId 查找完整请求链路
grep "req:abc-123-def" logs/app-*-INFO.log
```

## 生产环境排查

```bash
# 查看今天的错误
cat logs/app-$(date +%Y-%m-%d)-ERROR.log

# 按 requestId 追踪请求链路（跨天搜索）
grep "req:abc-123-def" logs/app-*-INFO.log

# 查看某个视图的所有日志（跨天搜索）
grep "apps.users.views" logs/app-*-INFO.log

# 实时监控今天的错误
tail -f logs/app-$(date +%Y-%m-%d)-ERROR.log

# 统计今天的错误数量
wc -l logs/app-$(date +%Y-%m-%d)-ERROR.log

# 删除 30 天前的日志（系统已自动清理，此命令仅用于手动干预）
find logs/ -name "app-*.log" -mtime +30 -delete
```

## 配置位置

| 文件 | 作用 |
|------|------|
| [common/logging.py](../django_edu_manage/common/logging.py) | `RequestIdFilter` + `DailyRotatingFileHandler` |
| [settings/logging_config.py](../django_edu_manage/settings/logging_config.py) | `get_logging_config()` — 根据环境变量构建 LOGGING 字典 |
| [settings/base.py](../django_edu_manage/settings/base.py) | 导入并设置 `LOGGING` |
| [middleware.py](../django_edu_manage/middleware.py) | `RequestIdMiddleware` — 设置 request_id |

## 架构图

```
请求到达
  │
  ▼
RequestIdMiddleware
  ├── 生成 UUID → request.request_id
  └── 存入 thread-local → RequestIdFilter 可用
  │
  ▼
视图 / 业务代码
  └── logger.info(...)  ──→  logging 系统
                              │
                              ├── DailyRotatingFileHandler
                              │     └── logs/app-{date}-{level}.log
                              │         ├── 跨天自动切换新文件
                              │         └── 超过 LOG_BACKUP 天自动清理
                              │
                              └── StreamHandler
                                    └── stdout (Docker/K8s 收集)
  │
  ▼
Response（meta.requestId = request.request_id）

日志文件:  logs/app-2025-06-01-INFO.log
  2025-06-01 12:00:00 [INFO] [apps.users.views] [req:abc-123] ...
响应体:   { "meta": { "requestId": "abc-123" } }
                 ▲ 一致，便于全链路追踪 ▲
```
