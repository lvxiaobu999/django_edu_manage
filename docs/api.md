# API 接口文档

## 约定

### 统一响应格式

所有接口返回以下结构：

```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": { ... },
    "meta": {
        "requestId": "uuid",
        "timestamp": "2025-01-01T00:00:00+00:00"
    }
}
```

| 字段 | 说明 |
|------|------|
| `success` | `true` 成功，`false` 失败 |
| `code` | 业务错误码，`0` 表示成功 |
| `message` | 人类可读的提示信息 |
| `data` | 实际载荷，列表/对象/null |
| `meta.requestId` | 请求追踪 ID，可用于日志关联 |
| `meta.timestamp` | 响应时间戳 |

### 认证方式

除登录/注册/刷新接口外，所有接口要求在请求头携带 JWT：

```
Authorization: Bearer <access_token>
```

### HTTP 状态码约定

| 状态码 | 含义 |
|--------|------|
| 200 | 所有业务响应（成功和失败都走 body 区分） |
| 400 | 请求参数格式错误 |
| 401 | access token 过期，需调用 refresh 接口或重新登录 |

---

## API 总览

```
认证模块 (apps/auth)
├── POST /api/login             登录
├── POST /api/logout            登出
├── POST /api/login/refresh     刷新 token
└── POST /api/register          注册

用户管理 (apps/users)
├── GET    /api/users            用户列表（分页）
├── POST   /api/users            创建用户
├── GET    /api/users/{id}       用户详情
├── PUT    /api/users/{id}       更新用户
├── DELETE /api/users/{id}       删除用户
├── POST   /api/users/{id}/approve  审核通过
└── GET    /api/users/pending    待审核用户列表

班级管理 (apps/classes)
├── GET    /api/classes          班级列表
├── POST   /api/classes          创建班级
├── GET    /api/classes/{id}     班级详情
├── PUT    /api/classes/{id}     更新班级
└── DELETE /api/classes/{id}     删除班级

师生简介 (apps/user_profile)
├── POST/GET/PUT  /api/profile/teacher  教师简介
└── POST/GET/PUT  /api/profile/student  学生简介

教研组 (apps/research_group)
├── GET    /api/research-groups          教研组列表
├── POST   /api/research-groups          创建教研组
├── GET    /api/research-groups/{id}     教研组详情
├── PUT    /api/research-groups/{id}     更新教研组
└── DELETE /api/research-groups/{id}     删除教研组

仪表盘 (apps/dashboard)
└── GET    /api/dashboard/stats          统计数据（支持 ?grade= 参数）
```

---

## 认证模块

详见 [docs/auth.md](auth.md)

---

## 用户管理

所有接口需要 `IsAuthenticated` + `IsApprovedAdmin` 权限。

### 用户列表 `GET /api/users`

查询参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `page` | 1 | 页码 |
| `size` | 10 | 每页条数（最大 100） |

响应：

```json
{
    "data": {
        "count": 150,
        "next": "/api/users?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "username": "admin01",
                "email": "admin@school.edu.cn",
                "phone": "",
                "role": "ADMIN",
                "role_display": "管理员",
                "real_name": "",
                "is_approved": true,
                "is_active": true,
                "date_joined": "2025-01-01T00:00:00Z"
            }
        ]
    }
}
```

### 审核通过 `POST /api/users/{id}/approve`

无需请求体。成功后用户 `is_approved=True`、`is_active=True`。

失败：

| 场景 | code | message |
|------|------|---------|
| 已审核通过 | 400 | 该用户已审核通过 |

### 待审核列表 `GET /api/users/pending`

返回 `is_approved=False` 的所有用户（不分页）。

---

## 班级管理

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `grade` | string | 年级枚举值，如 `GRADE_7` |
| `grade_display` | string | 年级中文名，如"七年级"（只读） |
| `name` | string | 班级名称，如"1班" |
| `headmaster` | int | 班主任 ID（可为 null） |
| `headmaster_name` | string | 班主任姓名（只读，无班主任时为空） |

### 年级枚举

| 值 | 中文 | 值 | 中文 |
|----|------|----|------|
| `GRADE_1` | 一年级 | `GRADE_7` | 七年级 |
| `GRADE_2` | 二年级 | `GRADE_8` | 八年级 |
| `GRADE_3` | 三年级 | `GRADE_9` | 九年级 |
| `GRADE_4` | 四年级 | `SENIOR_1` | 高一 |
| `GRADE_5` | 五年级 | `SENIOR_2` | 高二 |
| `GRADE_6` | 六年级 | `SENIOR_3` | 高三 |

---

## 师生简介

### 教师简介 `POST/GET/PUT /api/profile/teacher`

权限：`IsAuthenticated` + `IsRole('TEACHER')`

始终操作当前登录用户自己的简介，无需传用户 ID。

初始 POST 创建，再次 POST 即更新（有则更新，无则创建）。

```json
{
    "emp_no": "T001",
    "realname": "张三",
    "phone": "13800138000",
    "email": "zhangsan@school.edu.cn",
    "address": "北京市海淀区",
    "age": 35,
    "gender": "MALE",
    "research_groups": [1, 2],
    "class_ids": [1, 2, 3]
}
```

### 学生简介 `POST/GET/PUT /api/profile/student/`

权限：`IsAuthenticated` + `IsRole('STUDENT')`

逻辑同教师简介。

```json
{
    "stu_no": "S2025001",
    "realname": "李四",
    "phone": "13900139000",
    "email": "lisi@school.edu.cn",
    "address": "北京市朝阳区",
    "age": 14,
    "gender": "MALE",
    "class_id": 1
}
```

---

## 教研组

### 教研组列表 `GET /api/research-groups/`

```json
{
    "data": [
        { "id": 1, "name": "语文教研组" },
        { "id": 2, "name": "数学教研组" }
    ]
}
```

（未分页）

---

## 仪表盘

### 统计数据 `GET /api/dashboard/stats/`

全校统计（默认）：

```bash
GET /api/dashboard/stats/
```

某年级各班级人数：

```bash
GET /api/dashboard/stats/?grade=GRADE_7
```

响应结构见 [docs/dashboard.md](dashboard.md)

---

## 错误码参考

| code | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 业务错误（用户名密码错误、账户未激活等） |
| 400 | 请求参数校验失败 |

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [auth.md](auth.md) | 认证接口详情、Token 生命周期、前端集成 |
| [dashboard.md](dashboard.md) | 仪表盘接口文档 |
| [mvt-architecture.md](mvt-architecture.md) | Model/View/Serializer 三层架构 |
| [permissions_auth.md](permissions_auth.md) | 权限系统设计 |
| [response-middleware.md](response-middleware.md) | 统一响应格式原理 |
| [项目结构.md](项目结构.md) | 项目目录结构与模块关系 |
