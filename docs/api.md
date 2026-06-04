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

班级管理 (apps/classes)
├── GET    /api/classes          班级列表
├── POST   /api/classes          创建班级
├── GET    /api/classes/{id}     班级详情
├── PUT    /api/classes/{id}     更新班级
└── DELETE /api/classes/{id}     删除班级

师生简介 (apps/user_profile)
├── POST/GET/PUT  /api/profile/teacher  教师简介
└── POST/GET/PUT  /api/profile/student  学生简介

教研组 (apps/research_group)（待补充）

科目管理 (apps/subjects)
├── GET    /api/subjects          科目列表
├── POST   /api/subjects          创建科目
├── GET    /api/subjects/{id}     科目详情
├── PUT    /api/subjects/{id}     更新科目
└── DELETE /api/subjects/{id}     删除科目

学期管理 (apps/semester_dict)
├── GET    /api/semesters         学期列表
├── POST   /api/semesters         创建学期
├── GET    /api/semesters/{id}    学期详情
├── PUT    /api/semesters/{id}    更新学期
└── DELETE /api/semesters/{id}    删除学期

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

## 教研组

### 教研组列表 `GET /api/research-groups`

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

## 科目管理

基础字典，供考试、成绩模块引用。种子数据已包含中小学所有常见科目（语文、数学、英语等）。

### 科目列表 `GET /api/subjects`

```json
{
    "data": [
        { "id": 1, "name": "语文" },
        { "id": 2, "name": "数学" }
    ]
}
```

（未分页）

---

## 学期管理

基础字典，供考试模块引用。种子数据覆盖 2023-2024 ~ 2026-2027 四个学年共 8 个学期。

字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 唯一标识，如 `2025-2026-1` |
| `display_name` | string | 展示名称，如 `2025-2026学年第一学期` |

### 学期列表 `GET /api/semesters`

```json
{
    "data": [
        { "id": 1, "name": "2025-2026-1", "display_name": "2025-2026学年第一学期" },
        { "id": 2, "name": "2025-2026-2", "display_name": "2025-2026学年第二学期" }
    ]
}
```

（未分页）

---

## 考试管理

考试计划模块用于管理考试名称、类型、时间、年级、学期等元信息。与成绩表解耦，同一考试名称在不同学期/日期下是独立记录。

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
| `grade` | string | 年级枚举值，如 `SENIOR_1` |
| `semester` | int | 学期 ID（FK → Semester） |

> `name` 字段由学期 + 年级 + 考试类型自动拼接生成，如 `2025-2026学年第一学期高一期中考试`。

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

约束：同一学生 + 同一考试 + 同一科目只能有一条成绩记录。

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
| `subject` | int | 科目 ID（FK → Subjects） |
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
Score.student → StudentProfile.class_id → Classes.grade
                                  └──→ Classes.name
Score.exam → ExamPlan (考试类型/日期/年级/学期)
Score.subject → Subjects (科目名称)
```

通过这层关联，无需冗余存储即可按班级/年级/考试/科目等多维度查询和统计成绩。

---

## 仪表盘

### 统计数据 `GET /api/dashboard/stats`

全校统计（默认）：

```bash
GET /api/dashboard/stats
```

某年级各班级人数：

```bash
GET /api/dashboard/stats?grade=GRADE_7
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
