# Django 迁移操作实战

> 涵盖历史迁移记录 + 本次 user_profile → students/teachers 拆分全流程。

---

## 一、历史迁移序列

按执行顺序排列：

| 序号 | 迁移文件 | 类型 | 内容 |
|------|----------|------|------|
| 1 | `users/0001_initial` | schema | 创建 User 表 |
| 2 | `dicts/0001_initial` | schema | 创建 SubjectDict / SemesterDict / ResearchGroupDict / ClassDict 四张表 |
| 3 | `dicts/0002_initial` | schema | ClassDict.headmaster FK → TeacherProfile |
| 4 | `dicts/0003_seed_dicts` | data | 种子：19 科目 + 8 学期 |
| 5 | `dicts/0004_seed_classes` | data | 种子：102 班级 |
| 6 | `dicts/0005_seed_research_groups` | data | 种子：8 教研组 |
| 7 | `exam/0001_initial` | schema | 创建 ExamPlan 表 |
| 8 | `score/0001_initial` | schema | 创建 Score 基础表 |
| 9 | `score/0002_initial` | schema | Score.student FK → StudentProfile + 唯一约束 |
| 10 | `students/0001_initial` | schema | 创建 StudentProfile 表（原 user_profile 拆分） |
| 11 | `teachers/0001_initial` | schema | 创建 TeacherProfile 表（原 user_profile 拆分） |

> 历史记录：`user_profile` 模块已删除，其 3 个 migration（0001_initial / 0002_initial / 0003_seed_users_profiles）被 `students/0001_initial` + `teachers/0001_initial` 替代。种子数据 3060 学生 + 120 教师因 `db_table` 保持不变而保留。

---

## 二、user_profile → students + teachers 拆分全记录

### 2.1 背景

原 `apps/user_profile/` 同时包含 `TeacherProfile` 和 `StudentProfile` 两个模型。为降低模块耦合、独立管理学生和教师，拆分为两个独立 app。

### 2.2 Django 迁移核心概念

| 概念 | 说明 |
|------|------|
| **Migration 文件** | `apps/xxx/migrations/000N_xxx.py`，Python 代码描述表结构/数据变更 |
| **django_migrations 表** | 数据库元数据表，记录哪些 migration 已执行（app, name, applied 三列） |
| **makemigrations** | 对比模型和已有 migration，生成新的 migration 文件 |
| **migrate** | 执行未应用的 migration |
| **migrate --fake** | 只标记为"已应用"，不实际执行 SQL（表已存在时用） |
| **migrate --plan** | 预览迁移计划，不修改任何东西 |
| **dependencies** | migration 文件中的依赖声明，决定执行顺序 |

### 2.3 模型关系图

```
TeacherProfile ──M2M──> ResearchGroupDict (dicts)
TeacherProfile ──M2M──> ClassDict (dicts)
ClassDict ───────FK───> TeacherProfile (teachers)
                          ↑ 互相引用！这是循环依赖的根源

StudentProfile ──FK───> ClassDict (dicts)
Score ──────────FK───> StudentProfile (students)
```

### 2.4 操作步骤

#### 2.4.1 创建新模块

```bash
mkdir -p apps/students/migrations apps/teachers/migrations
touch apps/students/__init__.py apps/students/migrations/__init__.py
touch apps/teachers/__init__.py apps/teachers/migrations/__init__.py
```

> Django 只扫描带有 `__init__.py` 的 `migrations/` 目录。没有 `__init__.py` 就不会加载 migration 文件。

#### 2.4.2 编写模型 —— 保持 db_table

```python
# apps/students/models.py
class StudentProfile(models.Model):
    # ... 字段与原 user_profile 中完全一致 ...

    class Meta:
        db_table = 'student_profile'  # ← 关键！保持原表名
```

```python
# apps/teachers/models.py
class TeacherProfile(models.Model):
    # ... 字段与原 user_profile 中完全一致 ...

    class Meta:
        db_table = 'teacher_profile'  # ← 关键！保持原表名
```

**为什么要保持 `db_table`？**

Django 默认按 `{app_label}_{model_name}` 生成表名（如 `students_studentprofile`）。不显式指定的话：
1. Django 认为这是新表 → CREATE TABLE
2. 建表失败（表已存在）或建一张空表 → 数据丢失

保持 `db_table` = 新模型直接接管旧表，数据原封不动。

#### 2.4.3 更新 FK 字符串引用

```python
# apps/dicts/models.py —— 改前
headmaster = models.ForeignKey('user_profile.TeacherProfile', ...)
# 改后
headmaster = models.ForeignKey('teachers.TeacherProfile', ...)

# apps/score/models.py —— 改前
student = models.ForeignKey('user_profile.StudentProfile', ...)
# 改后
student = models.ForeignKey('students.StudentProfile', ...)
```

Django 的 `'app_label.ModelName'` 字符串引用在运行时延迟解析，改后无需改数据库列（FK 列存储的仍是 id 值）。

#### 2.4.4 更新配置

```python
# django_edu_manage/settings/base.py
INSTALLED_APPS = [
    # 'apps.user_profile.apps.UserProfileConfig',  ← 移除
    'apps.students.apps.StudentsConfig',          ← 新增
    'apps.teachers.apps.TeachersConfig',          ← 新增
]

# django_edu_manage/urls.py
# path('api/profile/', include('apps.user_profile.urls')),   ← 移除
path('api/', include('apps.students.urls')),                ← 新增
path('api/', include('apps.teachers.urls')),                ← 新增
```

#### 2.4.5 移除旧模块

```bash
mv apps/user_profile apps/_user_profile_backup
```

此时还不能 `rm -rf`，因为 `django_migrations` 表中仍有 `user_profile` 的 3 条记录，其他 migration 也依赖它。

#### 2.4.6 修复旧 migration 的依赖引用

`dicts/0002_initial.py` 和 `score/0002_initial.py` 的 `dependencies` 列表中包含 `('user_profile', '0001_initial')`，但该模块已移除，需要指向新 app：

```python
# apps/dicts/migrations/0002_initial.py
dependencies = [
    ('dicts', '0001_initial'),
    ('teachers', '0001_initial'),  # ← 原 ('user_profile', '0001_initial')
]
operations = [
    migrations.AddField(
        model_name='classdict',
        name='headmaster',
        field=models.ForeignKey(
            to='teachers.teacherprofile',  # ← 原 'user_profile.teacherprofile'
            ...
        ),
    ),
]

# apps/score/migrations/0002_initial.py
dependencies = [
    ('dicts', '0002_initial'),
    ('score', '0001_initial'),
    ('students', '0001_initial'),  # ← 原 ('user_profile', '0001_initial')
]
operations = [
    migrations.AddField(
        model_name='score',
        name='student',
        field=models.ForeignKey(
            to='students.studentprofile',  # ← 原 'user_profile.studentprofile'
            ...
        ),
    ),
]
```

**但这里有一个鸡生蛋问题**：`teachers` 和 `students` 的 migration 还没生成，现在就声明依赖会报 `NodeNotFoundError`。

#### 2.4.7 两阶段策略解决依赖问题

```
阶段一：临时去掉跨模块依赖
  → dicts/0002 暂时不依赖 teachers
  → score/0002 暂时不依赖 students
  → makemigrations students teachers（生成 0001_initial）
  → 恢复 dicts/0002 和 score/0002 的正确依赖

阶段二：解决循环依赖
  → teachers/0001 被 makemigrations 自动设了依赖 dicts/0005
  → dicts/0002 又依赖 teachers/0001
  → 形成环：teachers.0001 → dicts.0005 → ... → dicts.0002 → teachers.0001
  → 解决：将 teachers/0001 和 students/0001 的依赖降级到 dicts/0001
```

**为什么 makemigrations 把依赖设为 dicts/0005？**

因为 `TeacherProfile` 有 M2M 到 `ResearchGroupDict`，而 ResearchGroupDict 的种子数据在 `dicts/0005` 中。makemigrations 保守地把依赖设为 dicts 的最新 migration。

**为什么降级到 0001 就够了？**

M2M 只需要**目标表存在**即可。`dicts/0001_initial` 已经创建了 `ResearchGroupDict` 和 `ClassDict` 表。种子数据（0003/0004/0005）是 RUNPYTHON，和 schema 无关，不应成为依赖。

```python
# apps/teachers/migrations/0001_initial.py
dependencies = [
    ('dicts', '0001_initial'),       # ← 从 0005 降到 0001
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]

# apps/students/migrations/0001_initial.py
dependencies = [
    ('dicts', '0001_initial'),       # ← 同上
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]
```

#### 2.4.8 验证无循环依赖

```bash
python manage.py migrate --plan
# 错误 → 有循环
# "No planned migration operations." → 正确！
```

#### 2.4.9 手动清理 django_migrations 表

因为新 migration 对应的表已存在，不能真的执行 CREATE TABLE，需要 fake：

```python
from django.db import connection

with connection.cursor() as c:
    # 1. 删除旧模块的迁移记录
    c.execute("DELETE FROM django_migrations WHERE app = 'user_profile'")
    # 删除了 3 条：0001_initial / 0002_initial / 0003_seed_users_profiles

    # 2. 插入新模块的 fake 记录
    c.execute("INSERT INTO django_migrations (app, name, applied) "
              "VALUES ('students', '0001_initial', datetime('now'))")
    c.execute("INSERT INTO django_migrations (app, name, applied) "
              "VALUES ('teachers', '0001_initial', datetime('now'))")
```

**为什么不用 `migrate --fake`？**

`migrate --fake students 0001_initial` 也能达到同样效果。但本例中 migration 文件刚生成、依赖链刚修好、旧记录还需清理，手动 SQL 更可控。

**等效的 django-admin 命令**：

```bash
python manage.py migrate --fake students 0001_initial
python manage.py migrate --fake teachers 0001_initial
```

#### 2.4.10 清理和最终验证

```bash
rm -rf apps/_user_profile_backup

python manage.py check
# System check identified no issues (0 silenced).

python manage.py migrate --plan
# No planned migration operations.
```

---

## 三、指令速查

| 命令 | 作用 | 常用场景 |
|------|------|---------|
| `makemigrations` | 扫描模型 → 生成 migration | 新增/修改模型后 |
| `makemigrations <app>` | 只为指定 app 生成 | 只想生成部分 app |
| `migrate` | 执行所有未应用的 migration | 日常部署 |
| `migrate <app>` | 只迁移指定 app | 独立更新某模块 |
| `migrate --plan` | 预览要执行的操作 | **改 migration 后必跑** |
| `migrate --fake <app> <name>` | 标记已执行但不跑 SQL | 表已存在时接管 |
| `sqlmigrate <app> <name>` | 查看 migration 对应的 SQL | 审查 DDL |
| `check` | 系统检查（不检查迁移图） | 每次改模型后 |
| `showmigrations` | 列出所有 migration 状态 | 查看 [x] 已应用 / [ ] 未应用 |

---

## 四、核心原则

### 4.1 迁移依赖最小化

```
✅ 正确：FK 到 A → depends_on('A', '0001_initial')
✅ 正确：M2M 到 B → depends_on('B', '0001_initial')
❌ 错误：M2M 到 B → depends_on('B', '0005_seed_data')
```

M2M/FK 只需要目标表存在，`0001_initial` 已经建了表。种子数据是数据层的操作，不是 schema 依赖。

### 4.2 循环依赖的两条出路

```
方案 A（本次采用）：降级依赖
  只 depends_on 到对方的 0001，双方互不跨越

方案 B：拆分 migration
  A/0001: 纯自己的字段
  B/0001: 纯自己的字段
  A/0002: 加 FK 到 B（depends on B/0001）
  B/0002: 加 FK 到 A（depends on A/0002）  ← 无环！
```

### 4.3 保持 db_table 做模块迁移

```python
class Meta:
    db_table = 'original_table_name'  # 接管旧表
```

适用场景：模型在两个 app 间移动时，不想重建表/丢数据。

---

## 五、故障排查

| 错误信息 | 含义 | 排查方向 |
|---------|------|---------|
| `NodeNotFoundError: nonexistent parent node` | migration 依赖了不存在的 (app, name) | 检查 dependencies 中的 app_label 和 migration 编号 |
| `CircularDependencyError` | A→B→...→A 形成了环 | `migrate --plan` 看环上有哪些节点，降级依赖 |
| `table ... already exists` | migration 要 CREATE TABLE 但表已存在 | `migrate --fake` 或检查 `db_table` 设置 |
| `models.E028 db_table used by multiple models` | 两个模型声明了同一 `db_table` | 只保留一个模型，删除另一个 |
| `fields.E304 reverse accessor clashes` | related_name 重复 | 同模型只能存在一处 |
| `check` 通过但 `migrate` 失败 | 静态模型检查和迁移图是两套独立系统 | 用 `migrate --plan` 检查依赖链 |
