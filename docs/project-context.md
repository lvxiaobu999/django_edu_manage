# 项目上下文说明

## 项目概览

这是一个 Django 项目，项目名为 `django-edu-manage`。

当前项目已经具备：

- Django 基础项目结构
- 用户认证、班级管理、师生简介、教研组、仪表盘五大业务模块
- PostgreSQL 的 Docker Compose 配置
- 基于 `django-environ` 的环境变量配置
- 拆分后的 settings 模块

## 技术栈

- Python：`>=3.14`
- Django：`>=6.0.5`
- django-environ：用于读取 `.env` 配置
- PostgreSQL：通过 Docker Compose 启动
- uv：用于依赖管理和命令运行

## 目录结构

- `manage.py`
  - Django 命令入口
  - 会根据 `DJANGO_ENV` 自动选择 settings 模块

- `django_edu_manage/settings/`
  - Django 配置模块
  - `base.py`：公共配置
  - `development.py`：开发环境配置
  - `production.py`：生产环境配置
  - `__init__.py`：兼容 `django_edu_manage.settings` 写法

- `django_edu_manage/urls.py`
  - 全局路由入口

- `django_edu_manage/asgi.py`
  - ASGI 入口

- `django_edu_manage/wsgi.py`
  - WSGI 入口

- `templates/`
  - Django 模板目录

- `apps/`
  - 所有业务模块
  - `core/`：全局基础设施
  - `users/`：用户认证管理
  - `students/`：学生档案
  - `teachers/`：教师档案
  - `classes/`：班级管理
  - `research_group/`：教研组
  - `dashboard/`：统计仪表盘

- `docs/`
  - 项目开发文档

## 环境选择

默认环境是：

```text
development
```

默认启动：

```powershell
uv run python manage.py runserver
```

指定生产环境：

```powershell
$env:DJANGO_ENV='production'
uv run python manage.py check
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

## 数据库

Django 通过 `DATABASE_URL` 连接数据库。

PostgreSQL 示例：

```env
DATABASE_URL=postgres://django_user:django_password@localhost:5432/django_edu_manage
```

如果没有配置 `DATABASE_URL`，项目会回退到 SQLite。

## 当前开发阶段

项目目前还处于基础设施搭建阶段，适合继续做：

- 用户模型与登录
- 业务模型设计
- 聊天会话模型
- API 路由
- 后台管理配置
- 测试用例补充
