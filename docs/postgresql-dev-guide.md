# PostgreSQL 开发文档

## 目标

本次改造的目标是让项目支持 PostgreSQL，同时保留一个可直接启动的 SQLite 回退模式，避免数据库容器未启动时项目直接起不来。

## 本次修改内容

### 1. Django 数据库配置改成 PostgreSQL

修改文件：

- [django_edu_manage/settings.py](../django_edu_manage/settings.py)

改动说明：

- 通过 `DJANGO_DB_ENGINE` 控制当前使用 PostgreSQL 还是 SQLite
- 当 `DJANGO_DB_ENGINE=django.db.backends.postgresql` 时，使用 PostgreSQL
- 当未设置该环境变量时，自动回退到 SQLite，方便先把项目跑起来
- 数据库连接信息仍然保留环境变量写法，便于切换和部署

当前读取的环境变量如下：

- `DJANGO_DB_ENGINE`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

默认值如下：

- 数据库名：`django_edu_manage`
- 用户名：`django_user`
- 密码：`django_password`
- 主机：`localhost`
- 端口：`5432`

补充说明：

- 这次不是“强制所有环境都必须连 PostgreSQL”
- 这是为了让开发期更稳一些
- 你可以先直接运行项目，再单独启动 PostgreSQL 做切换练习

### 2. 增加 PostgreSQL Python 依赖

修改文件：

- [pyproject.toml](../pyproject.toml)

改动说明：

- 新增 `psycopg[binary]`
- 这是 Django 连接 PostgreSQL 的常用驱动之一

### 3. 增加 Docker Compose 文件

新增文件：

- [docker-compose.yml](../docker-compose.yml)

改动说明：

- 定义了一个 `postgres` 服务
- 使用 `postgres:16-alpine`
- 挂载了数据卷，保证容器重启后数据不丢失
- 暴露 `5432` 端口，方便本机连接
- 添加了健康检查，便于判断数据库是否可用

## Docker Compose 配置说明

当前 `docker-compose.yml` 的关键内容：

- 服务名：`postgres`
- 容器名：`django_edu_manage_postgres`
- 数据库名：`django_edu_manage`
- 用户名：`django_user`
- 密码：`django_password`
- 映射端口：`5432:5432`
- 数据卷：`postgres_data`

## 允许执行的命令

为了完成这次改造，允许使用的命令主要是这些：

### 1. 查看项目结构

```powershell
rg --files
```

用途：

- 查看项目里有哪些文件
- 判断是否已经存在 `docs/`、`docker-compose.yml`、数据库配置等内容

### 2. 搜索数据库相关配置

```powershell
rg -n "DATABASES|DATABASE_URL|psycopg|postgres"
```

用途：

- 查找当前项目里是否已经使用 PostgreSQL
- 查找是否已经有数据库环境变量配置
- 避免重复或冲突修改

### 3. 读取配置文件

```powershell
Get-Content pyproject.toml
Get-Content django_edu_manage\settings.py
```

用途：

- 读取依赖配置
- 读取 Django 数据库配置
- 确认修改位置

### 4. 语法检查

尝试执行过：

```powershell
python -m py_compile django_edu_manage\settings.py
py -3 -m py_compile django_edu_manage\settings.py
```

结果：

- 这两个命令都没有成功执行
- 报错信息是系统无法访问 `python.exe` / `py.exe`
- 这说明当前环境里的 Python 启动器可能存在权限或路径问题
- 因为 Python 命令本身没有跑起来，所以本次没有完成运行时验证

### 5. 编辑文件

本次通过代码编辑方式修改了：

- `pyproject.toml`
- `django_edu_manage/settings.py`
- `docker-compose.yml`
- `docs/postgresql-dev-guide.md`

说明：

- 文件内容按 UTF-8 保存
- 文档和备注使用中文
- 没有执行删除、重置、覆盖历史代码等危险操作

## 启动步骤

### 1. 启动 PostgreSQL

```powershell
docker compose up -d postgres
```

### 2. 安装 Python 依赖

```powershell
uv sync
```

如果你不用 `uv`，也可以按你自己的工具链安装依赖。

### 3. 执行迁移

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. 启动 Django

```powershell
python manage.py runserver
```

## 你需要知道的事情

- 如果没有设置 `DJANGO_DB_ENGINE`，项目会继续使用 SQLite
- 如果设置了 `DJANGO_DB_ENGINE=django.db.backends.postgresql`，就会尝试连接 PostgreSQL
- PostgreSQL 没启动时，只有在你显式切换到 PostgreSQL 模式后才会报错
- 这样做的好处是，学习和调试都更灵活

## 学习重点

这次改造最值得学的点有三个：

1. Django 数据库配置最好用环境变量管理
2. Docker Compose 适合把数据库这种外部依赖标准化
3. 文档里写清楚“改了什么、怎么启动、允许哪些命令”，后续协作会轻松很多

## 后续可以继续补的内容

- `.env` 文件示例
- Django 连接 PostgreSQL 的更完整配置
- 数据迁移流程说明
- 生产环境部署说明

## 官方参考

- Django 官方文档说明：Django 支持 PostgreSQL，并推荐使用 `django.db.backends.postgresql` 作为数据库后端；Django 6.0 文档中也说明 PostgreSQL 需要 `psycopg` 或 `psycopg2` 驱动，其中推荐 `psycopg`。
- Docker 官方 PostgreSQL 指南说明：PostgreSQL 容器需要配置 `POSTGRES_PASSWORD`，可以通过 `POSTGRES_USER` 和 `POSTGRES_DB` 指定默认用户和数据库；使用 volume 可以让数据在容器重启或重建后保留。
