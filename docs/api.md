# API 接口文档

> 在线文档：启动服务后访问 `http://127.0.0.1:8000/api/docs/`（Swagger UI）或 `http://127.0.0.1:8000/api/redoc/`（ReDoc）。

## 约定

### 统一响应格式

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
| `message` | 人类可读的提示信息（CRUD 操作返回中文："创建成功"/"更新成功"/"删除成功"等） |
| `data` | 实际载荷，列表/对象/null |
| `meta.requestId` | 请求追踪 ID，可用于日志关联 |
| `meta.timestamp` | 响应时间戳 |

### 认证方式

除登录/注册/刷新接口外，所有接口要求在请求头携带 JWT：

```
Authorization: Bearer <access_token>
```

### 路由约定

- 所有 API 路由末尾无斜杠（`NoSlashRouter` + `APPEND_SLASH = False`）
- RESTful 风格：复数资源名，如 `/api/users`、`/api/students`
- 列表接口默认分页（`?page=1&pageSize=10`），字典类接口返回全量
- 分页响应结构：`{"total": N, "page": 1, "pageSize": 10, "totalPages": M, "results": [...]}`

### HTTP 状态码约定

| 状态码 | 含义 |
|--------|------|
| 200 | 所有业务响应（成功和失败都走 body 的 `success` + `code` 区分） |
| 400 | 请求参数格式错误 |
| 401 | access token 过期，需调用 refresh 接口或重新登录 |

---

## API 总览

```
API 文档
├── GET    /api/schema/          OpenAPI 3.0 JSON
├── GET    /api/docs/            Swagger UI（可交互测试）
├── GET    /api/redoc/           ReDoc（只读文档）

枚举
├── GET    /api/choices           所有枚举
└── GET    /api/choices?key=roles   指定枚举

认证
├── POST   /api/login             登录
├── POST   /api/logout            登出
├── POST   /api/token_refresh     刷新 token
└── POST   /api/register          注册

用户管理（仅管理员）
├── GET    /api/users              用户列表（分页）
├── POST   /api/users              创建用户
├── GET    /api/users/{id}         用户详情
├── PUT    /api/users/{id}         全量更新用户
├── PATCH  /api/users/{id}         部分更新用户
├── DELETE /api/users/{id}         删除用户
├── POST   /api/users/{id}/approve   审核通过
└── GET    /api/users/pending      待审核用户列表

字典管理
├── /api/subjects           科目字典（完整 CRUD）
├── /api/semesters          学期字典（完整 CRUD）
├── /api/research-groups    教研组字典（完整 CRUD）
├── /api/classes            班级字典（完整 CRUD + grade/name/headmaster 筛选）
└── /api/classes/grade-classes   年级-班级级联数据

学生管理
├── GET    /api/students              学生列表（分页 + stu_no/realname/grade/class_id 筛选，仅管理员）
├── POST   /api/students              创建学生简介（管理员可为他人创建）
├── GET    /api/students/{id}         按 ID 查看详情
├── PUT    /api/students/{id}         全量更新
├── PATCH  /api/students/{id}         部分更新
└── DELETE /api/students/{id}         删除（仅管理员）

教师管理
├── GET    /api/teachers              教师列表（分页，仅管理员）
├── POST   /api/teachers              创建教师简介（管理员可为他人创建）
├── GET    /api/teachers/{id}         按 ID 查看详情
├── PUT    /api/teachers/{id}         全量更新
├── PATCH  /api/teachers/{id}         部分更新
└── DELETE /api/teachers/{id}         删除（仅管理员）

考试管理
└── /api/exams               考试计划（完整 CRUD + exam_type/grade/semester 筛选）

成绩管理
└── /api/scores              成绩记录（完整 CRUD）

仪表盘
└── /api/dashboard/stats     统计数据（支持 ?grade= 参数）
```

---

## 认证模块

详见 [auth.md](auth.md)。

### 登录 `POST /api/login`

```json
// 请求
{"username": "admin", "password": "z123456."}

// 响应
{
    "data": {
        "user": { "id": 1, "username": "admin", "role": "ADMIN", ... },
        "access": "eyJ...",
        "refresh": "eyJ..."
    }
}
```

### Token 刷新 `POST /api/token_refresh`

```json
// 请求
{"refresh": "eyJ..."}

// 响应
{"data": {"access": "eyJ...", "refresh": "eyJ..."}}
```

### 登出 `POST /api/logout`

```json
// 请求（需认证）
{"refresh": "eyJ..."}

// 响应
{"message": "已退出登录"}
```

### 注册 `POST /api/register`

```json
// 请求
{"username": "new_student", "password": "z123456.", "email": "s@school.cn", "role": "STUDENT"}

// 响应
{"data": { "id": 100, "username": "new_student", "is_approved": false, ... }}
```

> 注册后 `is_approved=False`，需管理员审核通过才能登录。

---

## 用户管理

所有接口需要 `IsAuthenticated` + `IsApprovedAdmin` 权限。

### 用户列表 `GET /api/users`

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `page` | 1 | 页码 |
| `pageSize` | 10 | 每页条数 |

### 审核通过 `POST /api/users/{id}/approve`

无需请求体。成功响应：

```json
{"success": true, "code": 0, "message": "ok", "data": { ... }}
```

已审核通过再次调用：

```json
{"success": false, "code": 400, "message": "该用户已审核通过"}
```

### 待审核列表 `GET /api/users/pending`

返回所有 `is_approved=False` 的用户。

---

## 字典管理

四个字典表均支持完整 CRUD（`GET list` / `POST create` / `GET {id}` / `PUT {id}` / `PATCH {id}` / `DELETE {id}`），无需认证之外的额外权限。

### 科目 `GET /api/subjects`

种子数据：语文、数学、英语、物理、化学、生物、地理、历史、政治、科学、体育、音乐、美术、信息技术、通用技术、劳动、综合实践、书法、心理健康（19 个）。

```json
{"data": [{"id": 1, "name": "语文"}, {"id": 2, "name": "数学"}]}
```

### 学期 `GET /api/semesters`

种子数据覆盖 2023-2024 ~ 2026-2027 四个学年（8 个学期）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 唯一标识，如 `2025-2026-1` |
| `display_name` | string | 展示名称，如 `2025-2026学年第一学期` |

### 教研组 `GET /api/research-groups`

种子数据：语文组、数学组、英语组、物理组、化学组、地理组、生物组、体育组（8 个）。

### 班级 `GET /api/classes`

种子数据：102 个班级（小学 6 级 × 10 班 + 初中 3 级 × 8 班 + 高中 3 级 × 6 班）。

**查询参数（均可选，可组合）：**

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `grade` | string | 年级编码精确匹配 | `?grade=GRADE_7` |
| `name` | string | 班级名忽略大小写模糊搜索 | `?name=1` → 匹配 "1班"、"10班" |
| `headmaster` | string | 班主任姓名忽略大小写模糊搜索 | `?headmaster=张` |

响应字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `grade` | string | 年级枚举值 |
| `grade_display` | string | 年级中文名（只读） |
| `name` | string | 班级名称 |
| `headmaster` | int | 班主任 ID（可为 null） |
| `headmaster_name` | string | 班主任姓名（只读） |

### 年级枚举

| 值 | 中文 | 值 | 中文 |
|----|------|----|------|
| `GRADE_1` | 一年级 | `GRADE_7` | 七年级 |
| `GRADE_2` | 二年级 | `GRADE_8` | 八年级 |
| `GRADE_3` | 三年级 | `GRADE_9` | 九年级 |
| `GRADE_4` | 四年级 | `SENIOR_1` | 高一 |
| `GRADE_5` | 五年级 | `SENIOR_2` | 高二 |
| `GRADE_6` | 六年级 | `SENIOR_3` | 高三 |

### 年级-班级联动 `GET /api/classes/grade-classes`

返回所有年级及其下班级的级联数据，用于前端年级-班级二级联动下拉。无需认证之外的额外权限。

```json
{
    "data": [
        {
            "grade_id": "GRADE_1",
            "grade_name": "一年级",
            "classes": [
                {"class_id": 1, "class_name": "1班"},
                {"class_id": 2, "class_name": "2班"}
            ]
        },
        {
            "grade_id": "GRADE_2",
            "grade_name": "二年级",
            "classes": []
        }
    ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `grade_id` | string | 年级编码（枚举值） |
| `grade_name` | string | 年级中文名 |
| `classes` | array | 该年级下的班级列表 |
| `classes[].class_id` | int | 班级 ID |
| `classes[].class_name` | string | 班级名称 |

> 无班级的年级也会返回，`classes` 为空数组，确保前端下拉选项完整。

---

## 学生管理

`apps/students` 模块，使用 `NoSlashRouter` 注册的 `StudentProfileViewSet`，支持完整 CRUD。

### 权限模型

| 操作 | 权限 |
|------|------|
| `list`（列表） | 仅 ADMIN |
| `create` | STUDENT + ADMIN |
| `retrieve`（按 ID 查看） | STUDENT + ADMIN |
| `update` / `partial_update` | STUDENT + ADMIN |
| `destroy`（删除） | 仅 ADMIN |

**数据隔离**：学生只能查看/编辑自己的简介。管理员可通过 URL 中的 `{id}` 操作任意学生。

### 接口列表

```
GET    /api/students             管理员查看所有学生（分页 + 筛选）；学生角色只返回自己的
POST   /api/students             创建学生简介
GET    /api/students/{id}        按学生 ID 查看详情
PUT    /api/students/{id}        全量更新
PATCH  /api/students/{id}        部分更新
DELETE /api/students/{id}        仅管理员
```

**学生列表查询参数（均可选，可组合）：**

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `stu_no` | string | 学号忽略大小写模糊搜索 | `?stu_no=2024` |
| `realname` | string | 姓名忽略大小写模糊搜索 | `?realname=张` |
| `grade` | string | 年级编码精确匹配 | `?grade=GRADE_7` |
| `class_id` | int | 班级 ID 精确匹配 | `?class_id=1` |

示例：
```
GET /api/students?grade=GRADE_7&class_id=3
→ 返回七年级 3 班的所有学生
```

### 创建 / 更新请求

```json
{
    "stu_no": "S2025001",
    "realname": "李四",
    "phone": "13900139000",
    "email": "lisi@school.edu.cn",
    "gender": "MALE",
    "class_id": 1
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user` | int | 否 | 目标用户 ID（管理员可为他人创建，非管理员自动设为自己） |
| `stu_no` | string | 是 | 学号，唯一 |
| `realname` | string | 是 | 真实姓名 |
| `phone` | string | 否 | 联系电话 |
| `email` | string | 否 | 邮箱 |
| `gender` | string | 否 | `MALE` / `FEMALE` |
| `class_id` | int | 否 | 班级 ID |

### 响应示例

```json
{
    "id": 242,
    "user": 242,
    "user_name": "student0001",
    "stu_no": "S2025001",
    "realname": "李四",
    "phone": "13800138000",
    "email": "lisi@school.edu.cn",
    "address": "",
    "age": 14,
    "gender": "MALE",
    "class_id": 1,
    "class_name": "1班",
    "grade": "GRADE_1",
    "grade_display": "一年级"
}
```

---

## 教师管理

`apps/teachers` 模块，使用 `NoSlashRouter` 注册的 `TeacherProfileViewSet`，支持完整 CRUD。

### 权限模型

| 操作 | 权限 |
|------|------|
| `list`（列表） | 仅 ADMIN |
| `create` | TEACHER + ADMIN |
| `retrieve`（按 ID 查看） | TEACHER + ADMIN |
| `update` / `partial_update` | TEACHER + ADMIN |
| `destroy`（删除） | 仅 ADMIN |

**数据隔离**：教师只能查看/编辑自己的简介。管理员可通过 URL 中的 `{id}` 操作任意教师。

### 接口列表

```
GET    /api/teachers             管理员查看所有教师（分页）；教师角色只返回自己的
POST   /api/teachers             创建教师简介
GET    /api/teachers/{id}        按教师 ID 查看详情
PUT    /api/teachers/{id}        全量更新
PATCH  /api/teachers/{id}        部分更新
DELETE /api/teachers/{id}        仅管理员
```

### 创建 / 更新请求

```json
{
    "emp_no": "T001",
    "realname": "张三",
    "phone": "13800138000",
    "email": "zhangsan@school.edu.cn",
    "gender": "MALE",
    "research_groups": [1, 2],
    "class_ids": [1, 2, 3]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user` | int | 否 | 目标用户 ID（管理员可为他人创建，非管理员自动设为自己） |
| `emp_no` | string | 是 | 工号，唯一 |
| `realname` | string | 是 | 真实姓名 |
| `phone` | string | 否 | 联系电话 |
| `email` | string | 否 | 邮箱 |
| `gender` | string | 否 | `MALE` / `FEMALE` |
| `research_groups` | [int] | 否 | 教研组 ID 列表 |
| `class_ids` | [int] | 否 | 所教班级 ID 列表 |

### 响应示例

```json
{
    "id": 122,
    "user": 122,
    "user_name": "teacher001",
    "emp_no": "T001",
    "realname": "张三",
    "phone": "13800138000",
    "email": "zhangsan@school.edu.cn",
    "address": "",
    "age": 35,
    "gender": "MALE",
    "research_groups": [1, 2],
    "research_group_names": ["语文组", "数学组"],
    "class_ids": [1, 2, 3]
}
```

---

## 考试管理

`name` 字段由学期 + 年级 + 考试类型自动拼接生成（如 `2025-2026学年第一学期高一期中考试`），创建时无需传。

### 考试类型枚举

| 值 | 中文 |
|----|------|
| `MONTHLY` | 月考 |
| `MOCK` | 模拟考 |
| `MIDTERM` | 期中 |
| `FINAL` | 期末 |

### 考试列表 `GET /api/exams`

**查询参数（均可选，可任意组合）：**

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `exam_type` | string | 考试类型枚举值 | `?exam_type=MIDTERM` |
| `grade` | string | 年级编码 | `?grade=GRADE_7` |
| `semester` | int | 学期 ID | `?semester=3` |

示例：
```
GET /api/exams?exam_type=MONTHLY&grade=SENIOR_1&semester=3
→ 返回 2025-2026学年第一学期高一月考
```

### 创建考试 `POST /api/exams`

```json
{
    "exam_type": "MIDTERM",
    "exam_date": "2026-04-20",
    "grade": "GRADE_7",
    "semester": 3
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `exam_type` | string | 是 | `MONTHLY` / `MOCK` / `MIDTERM` / `FINAL` |
| `exam_date` | date | 是 | 考试日期 |
| `grade` | string | 是 | 年级枚举值 |
| `semester` | int | 是 | 学期 ID（FK → SemesterDict） |

---

## 成绩管理

核心枢纽表，将学生、考试、科目绑定。同一学生 + 同一考试 + 同一科目只能有一条记录（唯一约束）。

### 录入成绩 `POST /api/scores`

```json
{
    "student": 242,
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
| `score` | decimal | 分数，一位小数，范围 0.0 ~ 999.9 |

### 成绩列表响应示例

```json
{
    "data": {
        "total": 34560,
        "page": 1,
        "pageSize": 10,
        "totalPages": 3456,
        "results": [
            {
                "id": 1,
                "student": 242,
                "student_name": "张三",
                "student_no": "S2025001",
                "exam": 1,
                "exam_name": "2025-2026学年第一学期一年级期中考试",
                "subject": 2,
                "subject_name": "数学",
                "score": 99.5
            }
        ]
    }
}
```

### 数据关系链

```
Score.student → StudentProfile.class_id → ClassDict.grade / ClassDict.name
Score.exam    → ExamPlan（考试类型 / 日期 / 年级 / 学期）
Score.subject → SubjectDict（科目名称）
```

---

## 仪表盘

### 统计数据 `GET /api/dashboard/stats`

| 参数 | 说明 |
|------|------|
| 无 | 返回全校各年级人数分布 |
| `?grade=GRADE_7` | 返回指定年级各班级人数 |

全校统计响应：

```json
{
    "data": {
        "totals": {"teachers": 120, "students": 3060, "classes": 102, "research_groups": 8},
        "distribution": [{"label": "一年级", "count": 300}, ...],
        "description": "各年级人数"
    }
}
```

详见 [dashboard.md](dashboard.md)。

---

## 枚举值

```
GET /api/choices               返回 roles / grades / exam_types / genders
GET /api/choices?key=roles      只返回角色枚举
```

```json
{"data": {"roles": [{"value": "ADMIN", "label": "管理员"}, ...]}}
```

---

## 完整使用流程

```
1. POST /api/register                注册账户，选择角色

2. POST /api/login                   获取 access_token + refresh_token
   后续请求 Header: Authorization: Bearer <access_token>

3. POST /api/students             完善学生简介（学生角色）
   或 POST /api/teachers            完善教师简介（教师角色）
   管理员可通过 POST /api/students 或 /api/teachers 为任意用户创建

4. 管理员 GET  /api/users/pending      查看待审核列表
5. 管理员 POST /api/users/{id}/approve   审核通过

6. access_token 过期后：
   POST /api/token_refresh             用 refresh token 换新 token

7. POST /api/logout                    登出，refresh token 加入黑名单
```

---

## 错误码参考

| code | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 业务错误（参数无效、用户不存在等） |
| 400 | 请求参数校验失败 |
| 401 | Token 无效或已过期（HTTP 401） |

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [auth.md](auth.md) | 认证接口详情、Token 生命周期 |
| [dict.md](dict.md) | 字典模块详述 |
| [dashboard.md](dashboard.md) | 仪表盘接口 |
| [jwt.md](jwt.md) | JWT 认证机制与轮转策略 |
| [permissions_auth.md](permissions_auth.md) | 权限系统设计 |
| [response-middleware.md](response-middleware.md) | 统一响应格式原理 |
| [项目结构.md](项目结构.md) | 项目目录结构与模块关系 |
| `/api/docs/` | Swagger UI 在线文档（需启动服务） |
