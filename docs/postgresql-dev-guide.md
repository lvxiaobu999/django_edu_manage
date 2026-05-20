# PostgreSQL 与环境配置开发文档

## 目标

本次改造的目标是把数据库配置从“写死在 `settings.py`”改成“通过 `.env` 系列文件管理”，这样你可以很自然地切换开发、测试和生产环境。

## 这次做了什么

### 1. Django 改成读取环境文件

修改文件：

- [django_edu_manage/settings.py](../django_edu_manage/settings.py)

核心逻辑：

- 先读取 `.env`
- 再按 `DJANGO_ENV` 读取 `.env.development` 或 `.env.production`
- 系统已经手工设置的环境变量优先，不会被文件覆盖

当前支持的环境变量：

- `DJANGO_ENV`
- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `DJANGO_DB_ENGINE`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

### 2. PostgreSQL 连接仍然保留

说明：

- 当 `DJANGO_DB_ENGINE=django.db.backends.postgresql` 时，Django 使用 PostgreSQL
- 不设置时，项目自动回退到 SQLite
- 这样可以先跑项目，再慢慢切 PostgreSQL

### 3. Docker Compose 也改成读环境变量

修改文件：

- [docker-compose.yml](../docker-compose.yml)

说明：

- PostgreSQL 的数据库名、用户名、密码、端口都改成变量
- 避免写死在 YAML 里
- 方便不同环境使用不同配置

### 4. 补了环境文件示例

新增文件：

- [.env.example](../.env.example)
- [.env.development.example](../.env.development.example)
- [.env.production.example](../.env.production.example)

说明：

- 这些是示例文件，适合提交到 Git
- 真正的 `.env`、`.env.development`、`.env.production` 不应该提交

### 5. 更新 `.gitignore`

修改文件：

- [`.gitignore`](../.gitignore)

新增忽略规则：

- `.env`
- `.env.*`
- `.idea/`
- `.vscode/`
- `db.sqlite3`
- `__pycache__/`

保留提交的文件：

- `.env.example`
- `.env.development.example`
- `.env.production.example`

## 环境文件怎么用

### 开发环境

创建 `.env.development`，内容可以参考 `.env.development.example`。

### 生产环境

创建 `.env.production`，内容可以参考 `.env.production.example`。

### 通用配置

创建 `.env`，放一些所有环境都通用的配置，比如基础密钥或默认值。

## 启动顺序

### 1. 安装依赖

```powershell
uv sync
```

### 2. 启动 PostgreSQL

```powershell
docker compose up -d postgres
```

### 3. 启动开发模式

```powershell
uv run python manage.py runserver
```

如果你想切到 PostgreSQL：

```powershell
$env:DJANGO_DB_ENGINE='django.db.backends.postgresql'
uv run python manage.py runserver
```

## 允许提交到 Git 的文件

- 业务代码
- 路由文件
- 文档
- 示例环境文件
- `docker-compose.yml`
- `pyproject.toml`
- `uv.lock`

## 不应该提交到 Git 的文件

- `.env`
- `.env.development`
- `.env.production`
- `db.sqlite3`
- `__pycache__/`
- `.idea/`
- `.vscode/`
- 临时日志和临时文件

## 学习重点

1. 配置不要写死在代码里
2. 开发、生产环境要分离
3. 示例文件和真实配置文件要分开管理
4. `settings.py` 最好只负责读取配置，不直接写死秘密信息

## 后续可以继续补的内容

- `.env` 真文件模板生成脚本
- 更完整的生产部署说明
- Django 与 PostgreSQL 的迁移流程说明
- 自动生成配置文件的脚本
