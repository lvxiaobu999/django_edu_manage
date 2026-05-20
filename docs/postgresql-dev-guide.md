# settings 模块与环境配置开发文档

## 目标

本次调整把原来的 `django_edu_manage/settings.py` 迁移为 `django_edu_manage/settings/` 模块，并支持在运行项目时通过 `DJANGO_ENV` 指定环境。

不指定环境时，默认使用 `development`。

## settings 模块结构

当前结构：

- `django_edu_manage/settings/base.py`
  - 公共配置
  - 读取 `.env` 系列文件
  - 配置 Django 应用、模板、数据库、静态文件等通用内容

- `django_edu_manage/settings/development.py`
  - 开发环境配置
  - 默认 `DEBUG=True`
  - 默认允许 `127.0.0.1` 和 `localhost`

- `django_edu_manage/settings/production.py`
  - 生产环境配置
  - 默认 `DEBUG=False`
  - 生产环境应明确配置 `SECRET_KEY`、`ALLOWED_HOSTS` 和数据库连接

- `django_edu_manage/settings/__init__.py`
  - 兼容 `django_edu_manage.settings` 这种默认写法
  - 会根据 `DJANGO_ENV` 自动导入 development 或 production

## 启动入口

这些文件已经支持按环境选择 settings：

- `manage.py`
- `django_edu_manage/asgi.py`
- `django_edu_manage/wsgi.py`

它们会读取：

```env
DJANGO_ENV=development
```

然后自动设置：

```text
django_edu_manage.settings.development
```

如果设置：

```env
DJANGO_ENV=production
```

则会使用：

```text
django_edu_manage.settings.production
```

## 环境文件约定

可以提交到 Git：

- `.env`
- `.env.development`
- `.env.production`

不提交到 Git：

- `.env.local`
- `.env.development.local`
- `.env.production.local`

命名理解：

- `.env`：通用默认配置
- `.env.development`：开发环境默认配置
- `.env.production`：生产环境默认配置
- `.local`：当前电脑自己的私有覆盖配置

## 配置加载顺序

配置优先级从低到高：

1. `.env`
2. `.env.development` 或 `.env.production`
3. `.env.local`
4. `.env.development.local` 或 `.env.production.local`
5. 系统环境变量

也就是说，本机 `.local` 文件可以覆盖团队默认配置，系统环境变量可以覆盖所有文件配置。

## 指定环境运行

### 默认开发环境

不指定 `DJANGO_ENV` 时默认就是开发环境：

```powershell
uv run python manage.py runserver
```

等价于：

```powershell
$env:DJANGO_ENV='development'
uv run python manage.py runserver
```

### 指定生产环境

```powershell
$env:DJANGO_ENV='production'
uv run python manage.py check
```

如果要临时绕过 `DJANGO_ENV`，也可以直接使用 Django 原生参数：

```powershell
uv run python manage.py check --settings=django_edu_manage.settings.production
```

## 数据库配置

Django 使用 `DATABASE_URL` 连接数据库。

PostgreSQL 示例：

```env
DATABASE_URL=postgres://django_user:django_password@localhost:5432/django_edu_manage
```

如果没有配置 `DATABASE_URL`，项目会回退到本地 SQLite。

Docker Compose 使用这些变量初始化 PostgreSQL：

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`

注意：

- `DATABASE_URL` 是 Django 用的
- `POSTGRES_*` 是 Docker PostgreSQL 容器用的
- 两边的用户名、密码和数据库名要保持一致

## Git 提交规则

应该提交：

- 业务代码
- 文档
- `docker-compose.yml`
- `pyproject.toml`
- `uv.lock`
- `.env`
- `.env.development`
- `.env.production`

不应该提交：

- `.env.local`
- `.env.development.local`
- `.env.production.local`
- `db.sqlite3`
- `__pycache__/`
- `.idea/`
- `.vscode/`

## 学习重点

1. `settings.py` 适合拆成 settings 模块
2. `base.py` 放公共配置
3. `development.py` 和 `production.py` 只放环境差异
4. `DJANGO_ENV` 负责选择运行环境
5. `.local` 文件负责本机私有覆盖
