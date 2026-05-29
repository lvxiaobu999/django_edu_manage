# Django 认证与权限系统详解

## 目录

1. [Django 内置认证系统](#1-django-内置认证系统)
2. [Django 内置权限系统](#2-django-内置权限系统)
3. [本项目自定义权限体系](#3-本项目自定义权限体系)
4. [如何创建管理员](#4-如何创建管理员)
5. [管理员是否需要审核](#5-管理员是否需要审核)
6. [DRF 权限类详解](#6-drf-权限类详解)
7. [完整注册-审核流程](#7-完整注册审核流程)
8. [参考资源](#8-参考资源)

---

## 1. Django 内置认证系统

### 1.1 核心概念

Django 的 `django.contrib.auth` 提供了开箱即用的用户认证系统：

```
django.contrib.auth
├── models.py          # User, Group, Permission 模型
├── authenticate()     # 验证用户名密码
├── login() / logout() # 登录/登出
├── backends.py        # 认证后端（可扩展）
└── hashers.py         # 密码哈希算法
```

### 1.2 AbstractUser 自带字段

继承 `AbstractUser` 后，模型自动拥有以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `username` | CharField(150) | 用户名 |
| `password` | CharField(128) | 密码（哈希存储，不是明文） |
| `email` | EmailField | 邮箱 |
| `first_name` | CharField(150) | 名 |
| `last_name` | CharField(150) | 姓 |
| `is_active` | BooleanField | 是否激活（False=禁止登录） |
| `is_staff` | BooleanField | 是否可访问 admin 后台 |
| `is_superuser` | BooleanField | 是否超级管理员（拥有所有权限） |
| `date_joined` | DateTimeField | 注册时间 |
| `last_login` | DateTimeField | 最后登录时间 |
| `groups` | M2M → Group | 所属用户组 |
| `user_permissions` | M2M → Permission | 个人权限 |

### 1.3 三个关键布尔字段

这是最容易混淆的三个字段：

```
is_active     → 控制"能否登录"
is_staff      → 控制"能否进 admin 后台"
is_superuser  → 控制"是否拥有所有权限"（不检查具体权限，一律通过）
```

典型组合：

| 场景 | is_active | is_staff | is_superuser |
|------|-----------|----------|--------------|
| 未审核用户 | False | False | False |
| 普通学生/教师 | True | False | False |
| 普通管理员 | True | True | False |
| 超级管理员 | True | True | True |

### 1.4 如何创建用户

```python
# 方式1：通过命令行（推荐用于创建超级管理员）
python manage.py createsuperuser

# 方式2：通过代码
from django.contrib.auth import get_user_model
User = get_user_model()

# 创建普通用户（密码自动哈希）
user = User.objects.create_user(
    username='admin01',
    password='secure_password',
    email='admin@school.edu.cn',
)

# 创建超级用户（is_staff=True, is_superuser=True）
user = User.objects.create_superuser(
    username='admin01',
    password='secure_password',
    email='admin@school.edu.cn',
)
```

**关键区别：**
- `create_user()` — 普通用户，`is_staff=False`, `is_superuser=False`
- `create_superuser()` — 超级用户，`is_staff=True`, `is_superuser=True`
- **绝对不要用 `User.objects.create()`** — 密码不会被哈希，登录时会失败

---

## 2. Django 内置权限系统

### 2.1 权限模型

Django 的权限是"每个模型 × 4 种操作"的粒度：

```
Permission 模型（存在 auth_permission 表中）：
  ├── content_type → 指向哪个模型
  ├── codename     → 权限代码名，如 'add_user', 'change_user'
  └── name         → 人类可读名称，如 'Can add user'
```

每个模型默认生成 4 个权限（由 Model.Meta.default_permissions 控制）：

| 权限 codename | 含义 | 示例 |
|---------------|------|------|
| `add_<model>` | 创建记录 | `add_user` |
| `change_<model>` | 修改记录 | `change_user` |
| `delete_<model>` | 删除记录 | `delete_user` |
| `view_<model>` | 查看记录 | `view_user` |

### 2.2 用户-权限关系

```
User ──M2M── Permission        (user_permissions，个人权限)
User ──M2M── Group ──M2M── Permission  (groups，组权限)
```

一个用户的最终权限 = 个人权限 + 所有所属组的权限。

### 2.3 代码中使用权限

```python
# 检查用户是否有某权限
user.has_perm('users.add_user')
user.has_perm('users.change_user')

# 在视图中检查（函数视图）
from django.contrib.auth.decorators import permission_required

@permission_required('users.add_user')
def my_view(request):
    ...

# 在 DRF 视图中
from rest_framework.permissions import DjangoModelPermissions

class MyViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    # 自动根据请求方法检查对应权限：
    #   GET    → view_<model>
    #   POST   → add_<model>
    #   PUT    → change_<model>
    #   DELETE → delete_<model>
```

### 2.4 Admin 后台与权限

Django Admin 是最能体现内置权限系统的地方：

```
Admin 访问要求（按优先级）：
  1. is_superuser=True   → 跳过所有权限检查，可以操作一切
  2. is_staff=True       → 可以进入 admin 后台
  3. 有具体权限          → 在 admin 中只能看到有权限的模型
```

在 Admin 中给某个用户分配权限：
1. 进入 `/admin/auth/user/`，点击用户
2. 在"用户权限"区域，勾选具体权限
3. 或把用户加入某个 Group（组），组带有预设的权限集合

---

## 3. 本项目自定义权限体系

### 3.1 与 Django 内置系统的关系

```
Django 内置                 本项目自定义
─────────────────────      ──────────────────
is_active                  保留：控制能否登录
is_staff                   （未使用，本项目用 role 字段代替）
is_superuser               （未使用）
role                       新增：ADMIN / TEACHER / STUDENT
is_approved                新增：审核状态
```

**为什么不用 `is_staff` 和 `is_superuser`？**
- 本项目的"管理员"是业务概念（role=ADMIN），不等同于 Django 的 staff/superuser
- 用自定义 `role` 字段可以精确控制 API 权限，不依赖 Django Admin
- 未来扩展（如增加"教务员"角色）只需加枚举值

### 3.2 项目中的三层权限体系

```
第 1 层：登录检查
  └── IsAuthenticated → request.user 必须已登录

第 2 层：角色检查
  └── IsRole('TEACHER') → request.user.role 必须等于指定角色

第 3 层：审核检查
  └── IsApprovedAdmin → role=ADMIN 且 is_approved=True
```

### 3.3 两套"管理员"的区别

| | Django 内置 Admin 后台管理员 | 本项目业务管理员 |
|---|---|---|
| 控制字段 | `is_staff` / `is_superuser` | `role='ADMIN'` / `is_approved` |
| 访问范围 | Django Admin 后台 (`/admin/`) | 业务 API (`/api/`) |
| 创建方式 | `createsuperuser` 命令或代码 | 注册 API 后审核通过 |
| 权限粒度 | Model 级别 (add/change/delete/view) | 接口级别 (自定义权限类) |
| 是否需要审核 | 不需要（代码直接创建） | 需要（`is_approved=True`） |

两种管理员互不冲突——一个人可以同时是业务管理员和 Django Admin 管理员，也可以只担任其一。

---

## 4. 如何创建管理员

### 4.1 创建 Django Admin 超级管理员

```bash
python manage.py createsuperuser
# 按提示输入用户名、邮箱、密码

# 或在 Django shell 中
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_superuser('admin', 'admin@school.edu.cn', 'password123')
```

这就是场景：`is_staff=True, is_superuser=True`，可以登录 `/admin/` 后台。

### 4.2 通过项目 API 创建业务管理员

本项目特有的流程——通过注册接口 + shell 手动激活：

```bash
# 步骤 1：打开 Django shell
python manage.py shell

# 步骤 2：创建业务管理员
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.create_user(
...     username='admin01',
...     password='admin123',
...     email='admin@school.edu.cn',
...     role='ADMIN',        # 业务角色：管理员
...     is_active=True,       # 激活账户
...     is_approved=True,     # 标记为已审核
... )
>>> user.save()
```

或者先通过 `/api/register/` 注册一个 ADMIN 账号，然后用已存在的管理员调用 `/api/{id}/approve/` 审核。这就引出了"先有鸡还是先有蛋"的问题——

**创建第一个管理员的标准做法：**

```bash
# 直接在 shell 中创建，绕过审核流程
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_user(
...     username='first_admin',
...     password='admin123',
...     role='ADMIN',
...     is_active=True,
...     is_approved=True,
... )

# 之后，这个管理员就可以通过 /api/{id}/approve/ 审核后续注册的用户
```

### 4.3 批量导入（未来可扩展）

```
方式 1：编写 Django management command
方式 2：Django Admin 后台操作
方式 3：通过 API + CSV 文件导入
```

---

## 5. 管理员是否需要审核

答案是：**取决于你怎么定义"管理员"。**

### 本项目规则

| 角色 | 是否需要审核 | 谁审核 |
|------|-------------|--------|
| STUDENT | 需要 | 已审核的 ADMIN |
| TEACHER | 需要 | 已审核的 ADMIN |
| ADMIN | 需要 | 已审核的 ADMIN |
| 第一个 ADMIN | 不需要（shell 直接创建） | — |

所以存在一个"引导问题"：第一个管理员必须通过 `python manage.py shell` 直接创建。

### 为什么管理员自己也要审核？

- 防止恶意注册管理员账号，API 层面无人审核就能操作
- Django Admin 的超级管理员和业务管理员分离——前者管理后台，后者管理 API

### 简化方案

如果觉得管理员互相审核太麻烦，可以修改 `IsApprovedAdmin` 权限类：

```python
class IsApprovedAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'ADMIN'
            # 去掉下面这行，管理员就不需要审核
            # and request.user.is_approved
        )
```

---

## 6. DRF 权限类详解

### 6.1 DRF 内置权限类

| 类 | 说明 | 适用场景 |
|----|------|---------|
| `AllowAny` | 不校验，直接放行 | 注册接口 |
| `IsAuthenticated` | 用户已登录（`request.user.is_authenticated`） | 内部 API |
| `IsAdminUser` | `user.is_staff` 为 True | Django Admin 相关 |
| `IsAuthenticatedOrReadOnly` | 登录或只读 | 公开列表页 |
| `DjangoModelPermissions` | 检查 model 级权限 | 需要细粒度权限控制 |
| `DjangoObjectPermissions` | 检查对象级权限 | 行级权限控制 |

### 6.2 本项目自定义权限类

```python
# apps/users/permissions.py

class IsApprovedAdmin(BasePermission):
    """三重检查：已登录 + role=ADMIN + 已审核"""
    # 用于 /api/ 用户管理和 /api/{id}/approve/ 审核操作

class IsRole(BasePermission):
    """角色检查：IsRole('TEACHER') 只允许教师访问"""
    # 用于 /api/profile/teacher/ 和 /api/profile/student/
```

### 6.3 权限检查优先级

Django REST Framework 检查权限的流程：

```
请求到达 → 认证（Authentication）
         → 权限检查（Permission） → 不通过 → 返回 403 Forbidden
         → 节流（Throttling）     → 通过
         → 进入视图
```

permission_classes 是 AND 关系：列表中所有类都必须通过。

```python
# 这两个必须同时满足：
permission_classes = [IsAuthenticated, IsApprovedAdmin]

# 等价于：
# 1. request.user.is_authenticated == True    (IsAuthenticated)
# 2. role == 'ADMIN' AND is_approved == True  (IsApprovedAdmin)
```

---

## 7. 完整注册-审核流程

```
┌─────────────────────────────────────────────────┐
│  1. 管理员初始化                                  │
│  $ python manage.py shell                        │
│  >>> User.objects.create_user(                   │
│      username='admin01', role='ADMIN',            │
│      is_active=True, is_approved=True)            │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│  2. 用户注册                                      │
│  POST /api/register/                             │
│  { "username":"zhangsan", "role":"STUDENT" }     │
│  → is_active=False, is_approved=False            │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│  3. 完善个人简介                                  │
│  POST /api/profile/student/                      │
│  { "stu_no":"S001", "realname":"张三" }          │
│  → 创建 StudentProfile                           │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│  4. 管理员查看待审核列表                           │
│  GET /api/pending/                               │
│  → 返回 is_approved=False 的所有用户              │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│  5. 管理员审核通过                                 │
│  POST /api/{id}/approve/                         │
│  → is_approved=True, is_active=True              │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│  6. 用户登录                                      │
│  用户名 + 密码 → 登录成功                          │
│  可以正常使用所有需要登录的接口                     │
└─────────────────────────────────────────────────┘
```

---

## 8. 参考资源

### 官方文档

| 资源 | 链接 |
|------|------|
| Django 认证系统概览 | https://docs.djangoproject.com/en/stable/topics/auth/ |
| 自定义用户模型 | https://docs.djangoproject.com/en/stable/topics/auth/customizing/ |
| Django Admin 文档 | https://docs.djangoproject.com/en/stable/ref/contrib/admin/ |
| 权限系统 | https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization |
| DRF 权限 | https://www.django-rest-framework.org/api-guide/permissions/ |
| DRF 认证 | https://www.django-rest-framework.org/api-guide/authentication/ |

### 推荐视频

| 主题 | 搜索关键词（YouTube / B站） |
|------|---------------------------|
| Django Auth 系统详解 | `Django authentication tutorial` |
| 自定义 User 模型 | `Django custom user model AbstractUser` |
| Django 权限管理 | `Django permissions and groups` |
| DRF 认证与权限 | `Django REST Framework permissions authentication` |
| Django Admin 定制 | `Django admin customization tutorial` |

### B站中文教程推荐

搜索以下关键词：
- `Django 用户认证系统`
- `Django 自定义用户模型 AbstractUser`
- `Django REST Framework 权限认证`
- `Django 后台管理 admin`

### 本项目相关文件

| 文件 | 说明 |
|------|------|
| [apps/users/models.py](../apps/users/models.py) | 自定义 User 模型 |
| [apps/users/permissions.py](../apps/users/permissions.py) | 自定义权限类 |
| [apps/users/views.py](../apps/users/views.py) | 注册、审核 API |
| [apps/users/serializers.py](../apps/users/serializers.py) | 序列化器 |
| [django_edu_manage/settings/base.py](../django_edu_manage/settings/base.py) | AUTH_USER_MODEL 配置 |
