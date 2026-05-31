# API 接口文档

## 基础说明

- 统一前缀：`/api/`
- Content-Type：`application/json`
- 认证方式：Session 认证（注册接口除外）

## 角色枚举

| 值 | 含义 |
|---|---|
| `ADMIN` | 管理员 |
| `TEACHER` | 老师 |
| `STUDENT` | 学生 |

## 年级枚举

| 值 | 含义 |
|---|---|
| `GRADE_1` ~ `GRADE_9` | 一年级 ~ 九年级 |
| `SENIOR_1` ~ `SENIOR_3` | 高一 ~ 高三 |

---

## 1. 注册

```
POST /api/register/
```

无需认证。注册后 `is_active=false`、`is_approved=false`，需管理员审核通过后方可登录。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，150字符以内 |
| password | string | 是 | 密码，最少6位 |
| email | string | 否 | 邮箱 |
| role | string | 是 | ADMIN / TEACHER / STUDENT |

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

---

## 2. 登录/登出

### 2.1 登录

```
POST /api/login/
```

无需认证。登录成功后建立 Session，浏览器自动保存 `sessionid` Cookie，后续请求自动携带该 Cookie 维持认证状态。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码，最少6位 |

### 请求示例

```json
{
  "username": "zhangsan",
  "password": "123456"
}
```

### 成功响应 `200 OK`

```json
{
  "id": 1,
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "phone": "",
  "role": "STUDENT",
  "role_display": "学生",
  "real_name": "",
  "is_approved": false,
  "is_active": false,
  "date_joined": "2026-05-26T10:00:00Z"
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 401 | 用户名或密码错误 |
| 403 | 账户未激活，请等待管理员审核 |

### 2.2 登出

```
POST /api/logout/
```

需要登录。清除服务端 Session，浏览器 `sessionid` Cookie 随之失效。

### 成功响应 `200 OK`

```json
{
  "detail": "已退出登录"
}
```

---

## 3. 用户管理（管理员）

### 3.1 用户列表

```
GET /api/
```

需要已审核通过的管理员。

### 3.2 用户详情

```
GET /api/{id}/
```

### 3.3 待审核用户列表

```
GET /api/pending/
```

需要已审核通过的管理员。

### 成功响应 `200 OK`

```json
[
  {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "phone": "",
    "role": "STUDENT",
    "role_display": "学生",
    "real_name": "",
    "is_approved": false,
    "is_active": false,
    "date_joined": "2026-05-26T10:00:00Z"
  }
]
```

### 3.4 审核通过

```
POST /api/{id}/approve/
```

需要已审核通过的管理员。将用户 `is_approved` 和 `is_active` 设为 `true`。

### 成功响应 `200 OK`

```json
{
  "id": 1,
  "username": "zhangsan",
  "role_display": "学生",
  "is_approved": true,
  "is_active": true
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 400 | 该用户已审核通过 |
| 404 | 用户不存在 |

---

## 4. 班级管理

### 4.1 班级列表

```
GET /api/classes/
```

需要登录。

### 4.2 班级详情

```
GET /api/classes/{id}/
```

### 4.3 创建班级

```
POST /api/classes/
```

需要登录。

```json
{
  "grade": "GRADE_7",
  "name": "1班"
}
```

### 4.4 更新班级

```
PUT /api/classes/{id}/
```

### 4.5 删除班级

```
DELETE /api/classes/{id}/
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 班级 ID |
| grade | string | 年级枚举值 |
| grade_display | string | 年级中文名 |
| name | string | 班级名称 |
| headmaster | int/null | 班主任 ID（关联 TeacherProfile） |
| headmaster_name | string | 班主任姓名 |

---

## 5. 老师简介

### 5.1 完善 / 查看老师简介

```
POST /api/profile/teacher/
GET  /api/profile/teacher/
```

需要登录，仅 `TEACHER` 角色可调用。首次 POST 创建，已存在则更新。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| emp_no | string | 是 | 工号，唯一 |
| realname | string | 是 | 真实姓名 |
| phone | string | 否 | 联系电话 |
| email | string | 否 | 邮箱 |
| address | string | 否 | 家庭住址 |
| research_groups | int[] | 否 | 所属教研组 ID 列表 |
| class_ids | int[] | 否 | 所教班级 ID 列表 |

### 请求示例

```json
{
  "emp_no": "T2026001",
  "realname": "张老师",
  "phone": "13800001111",
  "email": "zhang@example.com",
  "address": "北京市朝阳区",
  "research_groups": [1, 2],
  "class_ids": [1, 2]
}
```

### 成功响应 `200/201`

```json
{
  "id": 1,
  "user": 2,
  "user_name": "zhangsan",
  "emp_no": "T2026001",
  "realname": "张老师",
  "phone": "13800001111",
  "email": "zhang@example.com",
  "address": "北京市朝阳区",
  "research_groups": [1, 2],
  "research_group_names": ["数学教研组", "英语教研组"],
  "class_ids": [1, 2]
}
```

---

## 6. 学生简介

### 6.1 完善 / 查看学生简介

```
POST /api/profile/student/
GET  /api/profile/student/
```

需要登录，仅 `STUDENT` 角色可调用。首次 POST 创建，已存在则更新。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stu_no | string | 是 | 学号，唯一 |
| realname | string | 是 | 真实姓名 |
| phone | string | 否 | 联系电话 |
| email | string | 否 | 邮箱 |
| address | string | 否 | 家庭住址 |
| class_id | int | 否 | 所在班级 ID |

### 请求示例

```json
{
  "stu_no": "S2026001",
  "realname": "张三",
  "phone": "13900002222",
  "class_id": 1
}
```

### 成功响应 `200/201`

```json
{
  "id": 1,
  "user": 3,
  "user_name": "zhangsan",
  "stu_no": "S2026001",
  "realname": "张三",
  "phone": "13900002222",
  "email": "",
  "address": "",
  "class_id": 1,
  "class_name": "七年级1班"
}
```

---

## 7. 教研组管理

```
GET    /api/profile/research-groups/
POST   /api/profile/research-groups/
GET    /api/profile/research-groups/{id}/
PUT    /api/profile/research-groups/{id}/
DELETE /api/profile/research-groups/{id}/
```

需要登录。

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 教研组名称，唯一 |

---

## 完整使用流程

```
1. POST /api/register/           → 注册账户，选择角色

2. POST /api/profile/teacher/     → 根据角色完善对应简介（二选一）
   或 POST /api/profile/student/

3. 管理员 GET  /api/pending/      → 查看待审核列表
4. 管理员 POST /api/{id}/approve/ → 审核通过，账户激活

5. POST /api/login/               → 登录，获取 sessionid Cookie
6. 携带 Cookie 访问其他 API       → 正常使用需要登录的接口
7. POST /api/logout/              → 登出，退出登录
```
