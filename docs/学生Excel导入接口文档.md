# 学生 Excel 导入接口文档

## 一、接口概览

| 项目 | 说明 |
|------|------|
| 接口地址 | `POST /api/students/import-excel` |
| 权限 | 仅管理员 |
| 请求类型 | `multipart/form-data` |
| 文件格式 | `.xlsx` |
| 作用 | 批量创建学生用户账号和学生档案 |

导入采用“先校验、后写入”的方式：系统会先检查整张 Excel，任意一行存在错误时，本次导入不会写入任何数据，并返回错误行号和字段。

## 二、模板下载接口

客户端导入前应先下载系统提供的模板，按模板填写后再上传导入。

| 项目 | 说明 |
|------|------|
| 接口地址 | `GET /api/students/import-template` |
| 权限 | 仅管理员 |
| 响应类型 | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| 文件名 | `student_import_template.xlsx` |

请求示例：

```bash
curl -X GET "http://127.0.0.1:8000/api/students/import-template" \
  -H "Authorization: Bearer <access_token>" \
  -o student_import_template.xlsx
```

模板内容：

- `学生导入模板` sheet：包含表头和示例数据。
- `填写说明` sheet：说明必填列、性别取值、年级编码、班级匹配规则和导入策略。

## 三、导入请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | 是 | 学生信息 Excel 文件，仅支持 `.xlsx` |
| `default_password` | string | 否 | Excel 中未填写“密码/初始密码”时使用的默认密码，默认 `z123456.` |

请求示例：

```bash
curl -X POST "http://127.0.0.1:8000/api/students/import-excel" \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@students.xlsx" \
  -F "default_password=z123456."
```

## 四、Excel 模板说明

第一行必须是表头。支持中文表头，也支持部分英文别名。

### 必填列

| 字段 | 支持表头 | 说明 |
|------|----------|------|
| 学号 | `学号`、`stu_no`、`student_no` | 学生档案唯一标识，不可重复 |
| 姓名 | `姓名`、`真实姓名`、`realname`、`name` | 学生真实姓名 |

### 可选列

| 字段 | 支持表头 | 说明 |
|------|----------|------|
| 用户名 | `用户名`、`账号`、`username` | 不填时默认使用学号作为用户名 |
| 手机号 | `手机号`、`手机`、`联系电话`、`phone` | 同步写入用户和学生档案 |
| 邮箱 | `邮箱`、`email` | 同步写入用户和学生档案 |
| 地址 | `地址`、`家庭住址`、`address` | 写入学生档案 |
| 年龄 | `年龄`、`age` | 必须是 1 到 150 的整数 |
| 性别 | `性别`、`gender` | 支持 `男`、`女`、`MALE`、`FEMALE` |
| 班级ID | `班级ID`、`class_id` | 优先按班级 ID 匹配 |
| 年级 | `年级`、`grade` | 不填班级 ID 时，可配合“班级”匹配 |
| 班级 | `班级`、`班级名称`、`class_name` | 不填班级 ID 时，可配合“年级”匹配 |
| 密码 | `密码`、`初始密码`、`password` | 不填时使用请求参数 `default_password` |

## 五、班级匹配规则

优先级如下：

1. 如果填写 `班级ID/class_id`，系统优先按班级 ID 匹配。
2. 如果未填写班级 ID，但填写了 `年级 + 班级`，系统按 `ClassDict.grade + ClassDict.name` 匹配。
3. 如果班级信息全部为空，允许导入，学生档案的班级为空。

年级编码需要使用系统枚举值，例如：

```text
GRADE_1, GRADE_2, GRADE_3, GRADE_4, GRADE_5, GRADE_6,
GRADE_7, GRADE_8, GRADE_9,
SENIOR_1, SENIOR_2, SENIOR_3
```

## 六、导入行为

每一行会创建两类数据：

- `User`
  - `role = STUDENT`
  - `is_active = True`
  - `is_approved = True`
  - 用户名默认为学号

- `StudentProfile`
  - 绑定刚创建的用户
  - 写入学号、姓名、手机号、邮箱、地址、年龄、性别、班级等信息

系统会校验：

- 学号不能为空。
- 姓名不能为空。
- 用户名不能和已有用户重复。
- 学号不能和已有学生档案重复。
- Excel 内部用户名不能重复。
- Excel 内部学号不能重复。
- 年龄必须是 1 到 150 的整数。
- 性别必须是支持值。
- 班级 ID 或年级 + 班级名称必须能匹配到班级。

## 七、成功响应

```json
{
  "success": true,
  "code": 0,
  "message": "导入成功",
  "data": {
    "total_rows": 2,
    "imported_count": 2,
    "failed_count": 0,
    "errors": []
  },
  "meta": {
    "requestId": "...",
    "timestamp": "..."
  }
}
```

## 八、失败响应

只要存在错误行，本次导入不会写入任何数据。错误信息按行聚合，同一行多个错误会放在同一个 `messages` 集合中。

```json
{
  "success": false,
  "code": 400,
  "message": "导入失败，请根据 errors 修正 Excel 后重新上传",
  "data": {
    "total_rows": 2,
    "imported_count": 0,
    "failed_count": 1,
    "errors": [
      {
        "row": 3,
        "stu_no": "20260002",
        "realname": "李四",
        "messages": [
          "用户名已存在",
          "学号已存在"
        ]
      }
    ]
  },
  "meta": {
    "requestId": "...",
    "timestamp": "..."
  }
}
```

## 九、推荐模板

```text
学号 | 姓名 | 性别 | 年龄 | 手机号 | 邮箱 | 年级 | 班级 | 密码
20260001 | 张三 | 男 | 13 | 13800000001 | zhangsan@example.com | GRADE_7 | 1班 | z123456.
20260002 | 李四 | 女 | 13 | 13800000002 | lisi@example.com | GRADE_7 | 1班 |
```
