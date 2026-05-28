# 注册、角色简介与审核接口文档

## 基础说明

- 所有接口统一前缀：`/api/`
- Content-Type：`application/json`
- 认证方式：Session 认证（注册接口除外）

## 全局枚举

`role` 字段可选值：

| 值 | 含义 |
|---|------|
| `STUDENT` | 学生 |
| `TEACHER` | 老师 |
| `ADMIN` | 管理员 |

---

## 1. 注册

```
POST /api/register/
```

**无需认证。**

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，150字符以内 |
| password | string | 是 | 密码，最少6位 |
| email | string | 否 | 邮箱 |
| role | string | 是 | 角色：STUDENT / TEACHER / ADMIN |

### 请求示例

```json
{
  "username": "zhangsan",
  "password": "123456",
  "email": "zhangsan@example.com",
  "role": "STUDENT"
}
```

### 成功响应 `201 Created`

```json
{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "role": "STUDENT"
}
```

### 注意事项

- 注册后 `is_active` 为 `false`，`is_approved` 为 `false`，账户不可登录
- 需管理员审核通过后方可登录

---

## 2. 完善学生简介

```
POST /api/profile/student/
```

**需要登录。** 仅角色为 `STUDENT` 的用户可调用。每人只能完善一次。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| student_id | string | 是 | 学号，唯一 |
| class_group | int | 否 | 所属班级 ID |
| guardian_phone | string | 否 | 家长联系方式 |

### 请求示例

```json
{
  "student_id": "2026001",
  "class_group": 1,
  "guardian_phone": "13800001111"
}
```

### 成功响应 `201 Created`

```json
{
  "student_id": "2026001",
  "class_group": 1,
  "guardian_phone": "13800001111"
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 401 | 未登录 |
| 403 | 角色不是学生 |
| 400 | 已完善过简介 / 参数校验失败 |

---

## 3. 完善教师简介

```
POST /api/profile/teacher/
```

**需要登录。** 仅角色为 `TEACHER` 的用户可调用。每人只能完善一次。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| department | string | 是 | 教研组 |
| hire_date | string | 否 | 入职时间，格式 YYYY-MM-DD |

### 请求示例

```json
{
  "department": "数学教研组",
  "hire_date": "2025-09-01"
}
```

### 成功响应 `201 Created`

```json
{
  "department": "数学教研组",
  "hire_date": "2025-09-01"
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 401 | 未登录 |
| 403 | 角色不是老师 |
| 400 | 已完善过简介 / 参数校验失败 |

---

## 4. 完善管理员简介

```
POST /api/profile/admin/
```

**需要登录。** 仅角色为 `ADMIN` 的用户可调用。每人只能完善一次。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| employee_id | string | 是 | 工号，唯一 |
| id_card | string | 是 | 身份证号，18位，唯一 |

### 请求示例

```json
{
  "employee_id": "A2026001",
  "id_card": "320102199001011234"
}
```

### 成功响应 `201 Created`

```json
{
  "employee_id": "A2026001",
  "id_card": "320102199001011234"
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 401 | 未登录 |
| 403 | 角色不是管理员 |
| 400 | 已完善过简介 / 参数校验失败 |

---

## 5. 待审核用户列表

```
GET /api/users/pending/
```

**需要登录，** 仅已审核通过的管理员可查看。

### 成功响应 `200 OK`

```json
[
  {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "role": "STUDENT",
    "role_display": "学生",
    "real_name": "",
    "phone_number": "",
    "is_approved": false,
    "is_active": false,
    "date_joined": "2026-05-23T10:00:00Z"
  }
]
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 401 | 未登录 |
| 403 | 不是管理员 / 管理员本人未审核 |

---

## 6. 审核通过

```
POST /api/users/{id}/approve/
```

**需要登录，** 仅已审核通过的管理员可操作。

### 路径参数

| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 用户 ID |

### 成功响应 `200 OK`

```json
{
  "id": 1,
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "role": "STUDENT",
  "role_display": "学生",
  "real_name": "",
  "phone_number": "",
  "is_approved": true,
  "is_active": true,
  "date_joined": "2026-05-23T10:00:00Z"
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 401 | 未登录 |
| 403 | 不是管理员 / 管理员本人未审核 |
| 404 | 用户不存在 |
| 400 | 该用户已审核通过 |

---

## 完整使用流程

```
1. POST /api/register/           → 注册账户，选择角色
2. POST /api/profile/student/    → 根据角色完善对应简介（三选一）
   或 POST /api/profile/teacher/
   或 POST /api/profile/admin/
3. 管理员 GET /api/users/pending/   → 查看待审核列表
4. 管理员 POST /api/users/1/approve/ → 审核通过，账户激活
5. 用户可正常登录
```
