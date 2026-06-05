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

### 路由约定

- 所有 API 路由末尾无斜杠（`APPEND_SLASH = False`）
- RESTful 风格：复数资源名，如 `/api/users`、`/api/classes`
- 列表接口默认分页（`page` + `size` 参数），字典类接口不分页

### HTTP 状态码约定

| 状态码 | 含义 |
|--------|------|
| 200 | 所有业务响应（成功和失败都走 body 区分） |
| 400 | 请求参数格式错误 |
| 401 | access token 过期，需调用 refresh 接口或重新登录 |

---

## API 总览

```
基础枚举 (apps/core)
├── GET    /api/choices          所有枚举
└── GET    /api/choices?key=roles  指定枚举

认证模块 (apps/auth)
├── POST /api/login             登录
├── POST /api/logout            登出
├── POST /api/token_refresh     刷新 token
└── POST /api/register          注册

用户管理 (apps/users)
├── GET    /api/users            用户列表（分页）
├── POST   /api/users            创建用户
├── GET    /api/users/{id}       用户详情
├── PUT    /api/users/{id}       更新用户
├── DELETE /api/users/{id}       删除用户
├── POST   /api/users/{id}/approve  审核通过
└── GET    /api/users/pending    待审核用户列表

字典管理 (apps/dicts) —— 四合一基础字典
├── GET/POST/PUT/DELETE  /api/subjects          科目
├── GET/POST/PUT/DELETE  /api/semesters         学期
├── GET/POST/PUT/DELETE  /api/research-groups   教研组
├── GET/POST/PUT/DELETE  /api/classes           班级

师生简介 (apps/user_profile)
├── POST/GET/PUT  /api/profile/teacher  教师简介
└── POST/GET/PUT  /api/profile/student  学生简介

考试管理 (apps/exam)
├── GET    /api/exams             考试列表
├── POST   /api/exams             创建考试
├── GET    /api/exams/{id}        考试详情
├── PUT    /api/exams/{id}        更新考试
└── DELETE /api/exams/{id}        删除考试

成绩管理 (apps/score)
├── GET    /api/scores            成绩列表
├── POST   /api/scores            录入成绩
├── GET    /api/scores/{id}       成绩详情
├── PUT    /api/scores/{id}       更新成绩
└── DELETE /api/scores/{id}       删除成绩

仪表盘 (apps/dashboard)
└── GET    /api/dashboard/stats          统计数据（支持 ?grade= 参数）
```

---

## 认证模块

详见 [docs/auth.md](auth.md)

### 常见登录错误

| 状态码 | code | 说明 |
|--------|------|------|
| 200 | 1 | 用户名或密码错误 |
| 200 | 1 | 账户未激活，请等待管理员审核 |
| 401 | - | access token 过期，需调 refresh 接口 |

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

## 字典管理

> 科目、学期、教研组、班级四个基础字典统一归入 `apps/dicts` 模块。所有字典表已内置种子数据，可直接查询无需手动录入。

### 科目 `GET /api/subjects`

基础字典，供考试、成绩模块引用 FK。

种子数据包含中小学全科 19 个科目：语文、数学、英语、物理、化学、生物、地理、历史、政治、科学、体育、音乐、美术、信息技术、通用技术、劳动、综合实践、书法、心理健康。

```json
{
    "data": [
        { "id": 1, "name": "语文" },
        { "id": 2, "name": "数学" }
    ]
}
```

### 学期 `GET /api/semesters`

供考试模块引用 FK。种子数据覆盖 2023-2024 ~ 2026-2027 四个学年。

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 唯一标识，如 `2025-2026-1` |
| `display_name` | string | 展示名称，如 `2025-2026学年第一学期` |

```json
{
    "data": [
        { "id": 1, "name": "2025-2026-1", "display_name": "2025-2026学年第一学期" },
        { "id": 2, "name": "2025-2026-2", "display_name": "2025-2026学年第二学期" }
    ]
}
```

### 教研组 `GET /api/research-groups`

种子数据包含 8 个教研组：语文组、数学组、英语组、物理组、化学组、地理组、生物组、体育组。

```json
{
    "data": [
        { "id": 1, "name": "语文组" },
        { "id": 2, "name": "数学组" }
    ]
}
```

### 班级 `GET /api/classes`

种子数据包含 102 个班级：小学 6 级 × 10 班 + 初中 3 级 × 8 班 + 高中 3 级 × 6 班。

| 字段 | 类型 | 说明 |
|------|------|------|
| `grade` | string | 年级枚举值，如 `GRADE_7` |
| `grade_display` | string | 年级中文名（只读） |
| `name` | string | 班级名称，如 `1班` |
| `headmaster` | int | 班主任 ID（可为 null） |
| `headmaster_name` | string | 班主任姓名（只读，无班主任时为空） |

#### 年级枚举

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

### 学生简介 `POST/GET/PUT /api/profile/student`

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

## 考试管理

考试计划模块管理考试元信息。`name` 字段由学期 + 年级 + 考试类型自动拼接生成，无需手动填写。

### 考试类型枚举

| 值 | 中文 |
|----|------|
| `MONTHLY` | 月考 |
| `MOCK` | 模拟考 |
| `MIDTERM` | 期中 |
| `FINAL` | 期末 |

### 创建考试 `POST /api/exams`

```json
{
    "exam_type": "MONTHLY",
    "exam_date": "2026-03-15",
    "grade": "SENIOR_1",
    "semester": 1
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `exam_type` | string | 枚举值：`MONTHLY`/`MOCK`/`MIDTERM`/`FINAL` |
| `exam_date` | date | 考试日期 |
| `grade` | string | 年级枚举值 |
| `semester` | int | 学期 ID（FK → SemesterDict） |

> `name` 自动生成规则：`{学期display_name}{年级中文}{考试类型}` + 考试后缀（如考试类型已以"考"结尾则不重复添加）。
> 示例：`2025-2026学年第一学期高一期中考试`，`2026-2027学年第一学期高三月考`。

### 考试列表响应示例

```json
{
    "data": [
        {
            "id": 1,
            "name": "2025-2026学年第二学期高一月考",
            "exam_type": "MONTHLY",
            "exam_type_display": "月考",
            "exam_date": "2026-03-15",
            "grade": "SENIOR_1",
            "grade_display": "高一",
            "semester": 1,
            "semester_display": "2025-2026学年第二学期"
        }
    ]
}
```

---

## 成绩管理

核心枢纽表，将学生、考试、科目绑定。每条记录包含成绩分数。

约束：同一学生 + 同一考试 + 同一科目只能有一条成绩记录（unique constraint）。

### 录入成绩 `POST /api/scores`

```json
{
    "student": 1,
    "exam": 1,
    "subject": 2,
    "score": 99.5
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `student` | int | 学生 ID（FK → StudentProfile） |
| `exam` | int | 考试 ID（FK → ExamPlan） |
| `subject` | int | 科目 ID（FK → SubjectDict） |
| `score` | decimal | 分数，支持一位小数（0.0 ~ 999.9） |

### 成绩列表响应示例

```json
{
    "data": [
        {
            "id": 1,
            "student": 1,
            "student_name": "李四",
            "student_no": "S2025001",
            "exam": 1,
            "exam_name": "2025-2026学年第二学期高一月考",
            "subject": 2,
            "subject_name": "数学",
            "score": 99.5
        }
    ]
}
```

### 数据关系链

```
Score.student → StudentProfile.class_id → ClassDict.grade
                                        → ClassDict.name
Score.exam    → ExamPlan（考试类型/日期/年级/学期）
Score.subject → SubjectDict（科目名称）
```

---

## 仪表盘

### 统计数据 `GET /api/dashboard/stats`

全校统计（默认）：

```
GET /api/dashboard/stats
```

响应包含教师总数、学生总数、班级总数、教研组总数，以及各年级人数分布。

某年级各班级人数：

```
GET /api/dashboard/stats?grade=GRADE_7
```

响应详见 [docs/dashboard.md](dashboard.md)

---

## 枚举值

可通过 `/api/choices` 获取所有枚举值，前端无需硬编码。

```
GET /api/choices          返回全部：roles / grades / exam_types / genders
GET /api/choices?key=roles  只返回角色枚举
```

---

## 完整使用流程

```
1. POST /api/register             注册账户，选择角色

2. POST /api/login                获取 access_token + refresh_token
   后续请求带 Authorization: Bearer <access_token>

3. POST /api/profile/teacher      根据角色完善简介（教师或学生二选一）
   或 POST /api/profile/student

4. 管理员 GET  /api/users/pending    查看待审核列表
5. 管理员 POST /api/users/{id}/approve  审核通过

6. access_token 过期后：
   POST /api/token_refresh         用 refresh_token 换新 access_token

7. POST /api/logout                登出，refresh_token 加入黑名单
```

---

## 错误码参考

| code | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 业务错误（参数无效、用户不存在等） |
| 400 | 请求参数校验失败 |

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [auth.md](auth.md) | 认证接口详情、Token 生命周期、前端集成 |
| [dict.md](dict.md) | 字典模块详述（模型、枚举、种子数据） |
| [dashboard.md](dashboard.md) | 仪表盘接口文档 |
| [mvt-architecture.md](mvt-architecture.md) | Model/View/Serializer 三层架构 |
| [permissions_auth.md](permissions_auth.md) | 权限系统设计 |
| [response-middleware.md](response-middleware.md) | 统一响应格式原理 |
| [项目结构.md](项目结构.md) | 项目目录结构与模块关系 |
