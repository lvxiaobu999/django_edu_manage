# django_edu_manage - uv 常用指令速查表

本项目使用 uv 替代标准的 pip 和传统的虚拟环境工作流，极大地简化了 Python 的依赖管理 。在 Django 中使用 uv，不再需要手动激活虚拟环境，只需在标准的 Python 命令前加上 uv run，uv 就会自动在正确的、隔离的环境中执行它们 。

## 1. Django 核心执行命令
在日常的 Django 开发中，请使用 uv run 来执行 manage.py 。

检测项目：```bash uv run python manage.py check ```

启动开发服务器并指定环境：```bash uv run python manage.py check --settings=django_edu_manage.settings.production ```


启动开发服务器： ```bash uv run manage.py runserver ```


在指定端口启动服务器： ```bash uv run manage.py runserver 8080  ```


创建新的应用/模块： ```bash uv run manage.py startapp <app_name>  ```


生成迁移文件（修改模型后）： ```bash uv run manage.py makemigrations  ```


将迁移应用到数据库（迁移数据）： ```bash uv run manage.py migrate  ```


创建超级管理员用户： ```bash uv run manage.py createsuperuser  ```


打开 Django 交互式终端： ```bash uv run manage.py shell  ```


收集静态文件（用于生产环境）： ```bash uv run manage.py collectstatic  ```

## 2. 包与依赖管理
由于本项目包含 uv.lock 和 pyproject.toml 文件，请优先使用 uv add 和 uv remove 来管理包，而不是传统的 pip install 。


添加新包： ```bash uv add <package_name>  ```（例如：uv add djangorestframework） 


添加仅用于开发环境的包： ```bash uv add --dev <package_name> ```（例如：uv add --dev pytest-django） 


移除已有的包： ```bash uv remove <package_name>  ```


同步环境： ```bash uv sync ```（安装或更新所有内容，使其与你的 uv.lock 文件完全匹配；从 GitHub 拉取代码时非常有用） 


更新所有依赖： ```bash uv lock --upgrade ```（使用最新兼容的包版本更新 uv.lock 文件） 

## 3. 管理环境与 Python 版本

uv 可以动态获取并使用特定的 Python 版本，而不需要你在系统全局安装它们 。


使用特定 Python 版本运行命令： ```bash uv run --python 3.12 manage.py runserver ```


运行隔离的脚本而不影响项目环境： ```bash uv run script.py  ```


查看当前 uv 环境信息： ```bash uv info ```