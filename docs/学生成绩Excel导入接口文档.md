# 学生成绩 Excel 导入接口文档

## 一、接口概览

| 项目 | 说明 |
|------|------|
| 模板下载 | `GET /api/scores/import-template` |
| 成绩导入 | `POST /api/scores/import-excel` |
| 权限 | 已登录用户 |
| 导入请求类型 | `multipart/form-data` |
| 文件格式 | `.xlsx` |
| 作用 | 批量新增或覆盖更新学生成绩 |

导入采用“先校验、后写入”的方式：系统会先检查整张 Excel，任意一行存在错误时，本次导入不会写入任何数据，并返回错误行号、学号、姓名和错误信息集合。

## 二、模板下载接口

客户端导入前应先下载系统提供的模板。

```bash
curl -X GET "http://127.0.0.1:8000/api/scores/import-template" \
  -H "Authorization: Bearer <access_token>" \
  -o score_import_template.xlsx
```

模板包含：

- `成绩导入模板` sheet：填写学号、姓名、考试ID、科目ID、分数等。
- `填写说明` sheet：说明必填列、分数范围、重复成绩处理规则。
- `考试列表` sheet：列出系统已有考试 ID、考试名称、年级、考试日期。
- `科目列表` sheet：列出系统已有科目 ID、科目名称。

建议前端或用户优先填写 `考试ID` 和 `科目ID`，避免考试名称或科目名称重复导致无法唯一匹配。

## 三、导入请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | 是 | 学生成绩 Excel 文件，仅支持 `.xlsx` |
| `overwrite` | boolean | 否 | 已有成绩是否覆盖更新，默认 `false` |

请求示例：

```bash
curl -X POST "http://127.0.0.1:8000/api/scores/import-excel" \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@scores.xlsx" \
  -F "overwrite=false"
```

覆盖更新示例：

```bash
curl -X POST "http://127.0.0.1:8000/api/scores/import-excel" \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@scores.xlsx" \
  -F "overwrite=true"
```

## 四、Excel 列说明

第一行必须是表头。支持中文表头，也支持部分英文别名。

### 必填列

| 字段 | 支持表头 | 说明 |
|------|----------|------|
| 学号 | `学号`、`stu_no`、`student_no` | 用于匹配学生档案 |
| 分数 | `分数`、`成绩`、`score` | 0 到 999.9，最多 1 位小数 |

### 考试匹配列

`考试ID` 和 `考试名称` 二选一，推荐填写 `考试ID`。

| 字段 | 支持表头 | 说明 |
|------|----------|------|
| 考试ID | `考试ID`、`考试id`、`exam_id` | 优先按考试 ID 匹配 |
| 考试名称 | `考试名称`、`考试`、`exam_name` | 未填考试 ID 时按名称匹配；名称不唯一会报错 |

### 科目匹配列

`科目ID` 和 `科目名称` 二选一，推荐填写 `科目ID`。

| 字段 | 支持表头 | 说明 |
|------|----------|------|
| 科目ID | `科目ID`、`科目id`、`subject_id` | 优先按科目 ID 匹配 |
| 科目名称 | `科目名称`、`科目`、`subject_name` | 未填科目 ID 时按名称匹配；名称不唯一会报错 |

### 可选列

| 字段 | 支持表头 | 说明 |
|------|----------|------|
| 姓名 | `姓名`、`学生姓名`、`realname`、`name` | 可选；填写后会校验是否与学号对应学生一致 |

## 五、重复成绩处理

成绩唯一性由以下三项决定：

```text
学生 + 考试 + 科目
```

处理规则：

- `overwrite=false`：如果成绩已存在，返回错误，不写入任何数据。
- `overwrite=true`：如果成绩已存在，更新原成绩；如果不存在，新增成绩。
- Excel 内部如果出现同一学生、同一考试、同一科目重复，也会报错。

## 六、成功响应

```json
{
  "success": true,
  "code": 0,
  "message": "导入成功",
  "data": {
    "total_rows": 2,
    "imported_count": 2,
    "updated_count": 0,
    "failed_count": 0,
    "errors": []
  },
  "meta": {
    "requestId": "...",
    "timestamp": "..."
  }
}
```

覆盖更新时：

```json
{
  "success": true,
  "code": 0,
  "message": "导入成功",
  "data": {
    "total_rows": 2,
    "imported_count": 1,
    "updated_count": 1,
    "failed_count": 0,
    "errors": []
  },
  "meta": {
    "requestId": "...",
    "timestamp": "..."
  }
}
```

## 七、失败响应

错误信息按行聚合，同一行多个错误会放在同一个 `messages` 集合中。

```json
{
  "success": false,
  "code": 400,
  "message": "导入失败，请根据 errors 修正 Excel 后重新上传",
  "data": {
    "total_rows": 2,
    "imported_count": 0,
    "updated_count": 0,
    "failed_count": 1,
    "errors": [
      {
        "row": 2,
        "stu_no": "S20260001",
        "realname": "张三",
        "messages": [
          "该学生该考试该科目成绩已存在"
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

## 八、推荐模板

```text
学号 | 姓名 | 考试ID | 考试名称 | 科目ID | 科目名称 | 分数
S20260001 | 张三 | 1 | 2025-2026学年第一学期七年级期中考试 | 1 | 语文 | 95.5
S20260002 | 李四 | 1 | 2025-2026学年第一学期七年级期中考试 | 2 | 数学 | 88
```
