# 字典模块文档

## 概述

`apps/dicts/` 是项目的基础字典模块，将科目、学期、教研组、班级四个字典统一管理。所有字典表使用 `dict_` 前缀命名，表内数据通过 Data Migration 自动填充。

模块路径：`apps/dicts/`
路由前缀：`/api/`

## 模型

### SubjectDict — 科目字典

表名：`dict_subject`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `name` | CharField(100) | 科目名称，唯一 |

种子数据（19 条）：语文、数学、英语、物理、化学、生物、地理、历史、政治、科学、体育、音乐、美术、信息技术、通用技术、劳动、综合实践、书法、心理健康

被引用：`Score.subject`（FK，PROTECT）

### SemesterDict — 学期字典

表名：`dict_semester`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `name` | CharField(20) | 唯一标识，如 `2025-2026-1` |
| `display_name` | CharField(50) | 展示名称，如 `2025-2026学年第一学期` |

排序：`-name`（新学期在前）

种子数据（8 条），覆盖 2023-2027 四个学年：

| name | display_name |
|------|-------------|
| `2023-2024-1` | 2023-2024学年第一学期 |
| `2023-2024-2` | 2023-2024学年第二学期 |
| `2024-2025-1` | 2024-2025学年第一学期 |
| `2024-2025-2` | 2024-2025学年第二学期 |
| `2025-2026-1` | 2025-2026学年第一学期 |
| `2025-2026-2` | 2025-2026学年第二学期 |
| `2026-2027-1` | 2026-2027学年第一学期 |
| `2026-2027-2` | 2026-2027学年第二学期 |

被引用：`ExamPlan.semester`（FK，PROTECT）

### ResearchGroupDict — 教研组字典

表名：`dict_research_group`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `name` | CharField(100) | 教研组名称，唯一 |

种子数据（8 条）：语文组、数学组、英语组、物理组、化学组、地理组、生物组、体育组

被引用：`TeacherProfile.research_groups`（M2M）

### ClassDict — 班级字典

表名：`dict_class`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `grade` | CharField(20) | 年级，取自 GradeChoices 枚举 |
| `name` | CharField(50) | 班级名称，如 `1班` |
| `headmaster` | FK → TeacherProfile | 班主任，SET_NULL |

索引：`(grade, name)` 联合唯一约束
排序：`grade, name`

种子数据（102 条）：

| 学段 | 年级 | 班级数 |
|------|------|--------|
| 小学 | GRADE_1 ~ GRADE_6 | 各 10 班（1班~10班） |
| 初中 | GRADE_7 ~ GRADE_9 | 各 8 班（1班~8班） |
| 高中 | SENIOR_1 ~ SENIOR_3 | 各 6 班（1班~6班） |

被引用：
- `StudentProfile.class_id`（FK，SET_NULL）
- `TeacherProfile.class_ids`（M2M）
- `ClassDict.headmaster`（自引用 FK → TeacherProfile）

---

## 年级枚举（GradeChoices）

枚举定义在 `apps/dicts/models.py`，字段类型为 `models.TextChoices`，数据库存储左侧值。

| 数据库值 | 中文名 | 学段 |
|----------|--------|------|
| `GRADE_1` | 一年级 | 小学 |
| `GRADE_2` | 二年级 | 小学 |
| `GRADE_3` | 三年级 | 小学 |
| `GRADE_4` | 四年级 | 小学 |
| `GRADE_5` | 五年级 | 小学 |
| `GRADE_6` | 六年级 | 小学 |
| `GRADE_7` | 七年级 | 初中 |
| `GRADE_8` | 八年级 | 初中 |
| `GRADE_9` | 九年级 | 初中 |
| `SENIOR_1` | 高一 | 高中 |
| `SENIOR_2` | 高二 | 高中 |
| `SENIOR_3` | 高三 | 高中 |

`ClassDict.grade` 与 `ExamPlan.grade` 共用此枚举。

序列化器中通过 `get_{field}_display()` 自动生成 `grade_display` 只读字段（如 `GRADE_7` → `"七年级"`）。

---

## API 端点

所有端点使用 `NoSlashRouter`（路由末尾无斜杠）。字典接口不分页。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/subjects` | 科目列表 |
| POST | `/api/subjects` | 创建科目 |
| GET | `/api/subjects/{id}` | 科目详情 |
| PUT | `/api/subjects/{id}` | 更新科目 |
| DELETE | `/api/subjects/{id}` | 删除科目 |
| GET | `/api/semesters` | 学期列表（新学期在前） |
| POST | `/api/semesters` | 创建学期 |
| GET | `/api/semesters/{id}` | 学期详情 |
| PUT | `/api/semesters/{id}` | 更新学期 |
| DELETE | `/api/semesters/{id}` | 删除学期 |
| GET | `/api/research-groups` | 教研组列表 |
| POST | `/api/research-groups` | 创建教研组 |
| GET | `/api/research-groups/{id}` | 教研组详情 |
| PUT | `/api/research-groups/{id}` | 更新教研组 |
| DELETE | `/api/research-groups/{id}` | 删除教研组 |
| GET | `/api/classes` | 班级列表（含年级中文和班主任名） |
| POST | `/api/classes` | 创建班级 |
| GET | `/api/classes/{id}` | 班级详情 |
| PUT | `/api/classes/{id}` | 更新班级 |
| DELETE | `/api/classes/{id}` | 删除班级 |

---

## 模型关系总图

```
SubjectDict ──────────────────────┐
                                  │ FK (PROTECT)
                                  ▼
SemesterDict ──── FK (PROTECT) ── Score ─── FK (CASCADE) ── StudentProfile
                       │           ▲                          │
                       ▼           │                          │
ResearchGroupDict ◄── M2M ── TeacherProfile                  │
                       │           ▲                          │
                       ▼           │                          │
ClassDict ◄─── M2M ───────────────┘                          │
    │                                                        │
    │ FK (SET_NULL)                                          │
    │                                                        │
    └────────────────────────────────────────────────────────┘
    │                                                        │
    └── FK headmaster (SET_NULL) ──► TeacherProfile          │
                                                             │
ExamPlan ─── FK (CASCADE) ─────────────────────────────────────┘
    │
    └── FK semester (PROTECT) ──► SemesterDict
    └── grade 使用 GradeChoices（与 ClassDict.grade 共用）
```

---

## 删除保护策略

| 字典 | 被引用的 FK | on_delete | 说明 |
|------|-----------|-----------|------|
| SubjectDict | Score.subject | PROTECT | 有成绩记录时不允许删除 |
| SemesterDict | ExamPlan.semester | PROTECT | 有考试计划时不允删除 |
| ResearchGroupDict | TeacherProfile.research_groups | M2M | 设为空即可删除 |
| ClassDict | StudentProfile.class_id | SET_NULL | 删除班级时学生保留但班级置空 |
| ClassDict | TeacherProfile.class_ids | M2M | 设为空即可删除 |

## 种子数据迁移

所有种子数据以 Django Data Migration 方式提供，`python manage.py migrate` 后自动填充：

```
dicts/
├── 0003_seed_dicts.py           # 19 科目 + 8 学期
├── 0004_seed_classes.py         # 102 班级
└── 0005_seed_research_groups.py # 8 教研组
```

使用 `ignore_conflicts=True`，重复执行 migrate 不会报错。
