# 迁移记录

## 2026-05-28：教研组模块拆分

### 背景

将 `ResearchGroup` 模型从 `apps/user_profile/` 拆分到独立的 `apps/research_group/` 应用。

### 操作步骤

#### 1. 创建新 app

```
python manage.py startapp research_group apps/research_group
```

#### 2. 迁移模型

- 将 `ResearchGroup` 从 `user_profile/models.py` 移到 `research_group/models.py`
- 保持 `db_table = 'research_group'` 不变（确保表名一致）
- 更新 `TeacherProfile.research_groups` 的 M2M 字段指向新 app：
  ```python
  # 之前
  research_groups = models.ManyToManyField(ResearchGroup, ...)
  # 之后
  research_groups = models.ManyToManyField('research_group.ResearchGroup', ...)
  ```

#### 3. 更新引用

| 文件 | 操作 |
|------|------|
| `user_profile/serializers.py` | 移除 ResearchGroup import |
| `user_profile/views.py` | 移除 ResearchGroupViewSet |
| `user_profile/urls.py` | 移除 research-groups 路由 |
| `user_profile/admin.py` | 移除 ResearchGroupAdmin |
| `research_group/serializers.py` | 新建，ResearchGroupSerializer |
| `research_group/views.py` | 新建，ResearchGroupViewSet |
| `research_group/urls.py` | 新建，DefaultRouter 路由 |
| `research_group/admin.py` | 新建，ResearchGroupAdmin |
| `research_group/apps.py` | 修改 name 为 `apps.research_group` |
| `settings/base.py` | INSTALLED_APPS 新增研究组 app |
| `urls.py` | 新增 `/api/research-groups/` 路由 |

#### 4. 处理迁移文件

由于模型所属 app 变更，旧的迁移文件无法直接使用：

- 删除 `user_profile/migrations/` 下的旧迁移（0001~0003）
- 删除 `classes/migrations/` 下的旧迁移（0001~0002）
- 删除 `users/migrations/` 下的旧迁移（0001）
- 保留所有 `__init__.py`

#### 5. 重建数据库

重新执行 `makemigrations` + `migrate`，生成全新的迁移文件：

```
Migrations for 'research_group':
  0001_initial.py — Create model ResearchGroup

Migrations for 'classes':
  0001_initial.py — Create model Classes
  0002_initial.py — Add headmaster FK + unique constraint

Migrations for 'user_profile':
  0001_initial.py — Create model TeacherProfile, StudentProfile
  0002_initial.py — Add user FK + M2M fields

Migrations for 'users':
  0001_initial.py — Create model User
```

---

### 遇到的问题

#### 问题 1：数据库文件被锁定

**现象：** 尝试删除旧 `db.sqlite3` 时报错 `Device or resource busy`，无法删除或重命名文件。

**原因：** VSCode 的 Python 扩展或 SQLite 扩展持有文件句柄，即使关闭了所有终端，进程仍然占用。

**尝试过的方案：**
- `rm -f` — 失败
- `cmd.exe /c del /f` — 失败
- `os.remove()` via Python — PermissionError
- `mv` 重命名 — 失败
- `taskkill /F /IM python.exe` 杀死 4 个 Python 进程 — 仍失败（其他进程持有锁）

**最终方案：** 改用新数据库文件名 `db_v2.sqlite3`，避开锁定文件。

#### 问题 2：跨 app 迁移模型的正确姿势

**核心难点：** 模型从 A 应用迁移到 B 应用，同时 A 应用中还有其他模型通过 M2M 引用该模型。

**理论上正确的做法：**
1. 在新 app 创建模型（相同 db_table）
2. 通过 `SeparateDatabaseAndState` 操作，state 层面删除旧模型、创建新模型，database 层面不做任何操作
3. 修改 M2M 的 through 表引用

**实际选择的做法（开发阶段）：**
- 直接删库重建。开发初期数据量小，重建成本低。
- 生产环境应使用上述 `SeparateDatabaseAndState` 方式，保留数据。

#### 问题 3：AppConfig 的 name 命名

Django 的 `AppConfig.name` 需要是完整的 Python 包路径。当 app 放在 `apps/` 目录下时：

```python
# 错误
class ResearchGroupConfig(AppConfig):
    name = 'research_group'  # Django 找不到这个模块

# 正确
class ResearchGroupConfig(AppConfig):
    name = 'apps.research_group'  # 完整路径
```

`name` 的最后一节自动成为 `app_label`（即 `research_group`），用于 `AUTH_USER_MODEL = 'users.User'` 这种引用和数据库迁移。

---

### 经验总结

1. **开发阶段能删库就别折腾复杂迁移** — 数据量小、没有线上流量时，删库重建是最稳妥的方式
2. **生产环境用 `SeparateDatabaseAndState`** — 确保 state（Django 内部模型注册表）变更的同时，database 层面不做删表操作
3. **AppConfig.name 永远写全路径** — 否则 INSTALLED_APPS 和迁移都会出问题
4. **关闭 IDE 的数据库扩展** — VSCode 的 SQLite Viewer 之类会锁文件，开发时遇到文件锁定先检查是否有扩展占用了
