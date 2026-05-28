# 2026-05-23 注册 + 角色简介 + 审核接口

## 概述

实现用户注册、角色简介完善、管理员审核的完整流程。

## 依赖变更

- `pyproject.toml`：新增 `djangorestframework>=3.16`

## settings 变更

- `django_edu_manage/settings/base.py`：INSTALLED_APPS 新增 `rest_framework`

## 模型变更

- `apps/users/models.py`：
  - User 模型新增 `is_approved` 字段（BooleanField, default=False，审核状态）
  - 新增 `AdminProfile` 模型（OneToOne → User，employee_id 工号，id_card 身份证号）

## 新增文件

- `apps/users/serializers.py` — 所有序列化器
  - RegisterSerializer：注册（username, password, email, role）
  - StudentProfileSerializer：学生简介（student_id, class_group, guardian_phone）
  - TeacherProfileSerializer：教师简介（department, hire_date）
  - AdminProfileSerializer：管理员简介（employee_id, id_card）
  - UserSerializer：用户列表展示

- `apps/users/urls.py` — API 路由

## 变更文件

- `apps/users/views.py` — 重写为 DRF 视图
- `apps/users/admin.py` — 注册 AdminProfile 到后台
- `django_edu_manage/urls.py` — 新增 `/api/` 路由挂载

## API 接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/register/` | 注册用户，创建后 is_active=False | 无需登录 |
| POST | `/api/profile/student/` | 完善学生简介 | 已登录 + 学生角色 |
| POST | `/api/profile/teacher/` | 完善教师简介 | 已登录 + 老师角色 |
| POST | `/api/profile/admin/` | 完善管理员简介 | 已登录 + 管理员角色 |
| GET | `/api/users/pending/` | 查看待审核用户列表 | 管理员 + 已审核 |
| POST | `/api/users/<id>/approve/` | 审核通过（激活账户） | 管理员 + 已审核 |

## 注册-审核流程

1. 用户通过 `/api/register/` 注册，选择角色
2. 根据角色调用对应 profile 接口完善简介
3. 管理员调用审核接口激活账户

## 迁移

`users/0003_user_is_approved_adminprofile.py`
