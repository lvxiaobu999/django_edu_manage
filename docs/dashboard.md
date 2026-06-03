# 面板数据统计（仪表盘）
## API 端点

```
GET /api/dashboard/stats/          全校各年级人数分布（默认）
GET /api/dashboard/stats/?grade=GRADE_7  七年级下各班级人数
```

需要登录（`Authorization: Bearer <access_token>`）。

## 需求一：统计总数

响应中 `totals` 字段包含四项：

```json
{
    "totals": {
        "teachers": 50,
        "students": 1200,
        "classes": 60,
        "research_groups": 15
    }
}
```

| 字段 | 说明 |
|------|------|
| `teachers` | 教师总数 |
| `students` | 学生总数 |
| `classes` | 班级总数 |
| `research_groups` | 教研组数 |

## 需求二：年级/班级人数分布

前端做一个下拉选择框，切换不同的统计维度。

### 选择"全校"（默认）

不传 `grade` 参数，返回一年级到高三各年级学生人数：

```bash
GET /api/dashboard/stats/
```

```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {
        "totals": { "teachers": 50, "students": 1200, "classes": 60, "research_groups": 15 },
        "distribution": [
            { "label": "一年级", "count": 80 },
            { "label": "二年级", "count": 90 },
            { "label": "三年级", "count": 100 },
            { "label": "四年级", "count": 110 },
            { "label": "五年级", "count": 95 },
            { "label": "六年级", "count": 105 },
            { "label": "七年级", "count": 130 },
            { "label": "八年级", "count": 120 },
            { "label": "九年级", "count": 115 },
            { "label": "高一", "count": 100 },
            { "label": "高二", "count": 85 },
            { "label": "高三", "count": 70 }
        ],
        "description": "各年级人数"
    }
}
```

### 选择具体年级（如七年级）

传 `grade=GRADE_7`，返回该年级下各班级人数：

```bash
GET /api/dashboard/stats/?grade=GRADE_7
```

```json
{
    "data": {
        "totals": { ... },
        "distribution": [
            { "label": "七年级1班", "count": 45 },
            { "label": "七年级2班", "count": 42 },
            { "label": "七年级3班", "count": 43 }
        ],
        "description": "七年级各班级人数"
    }
}
```

## 年级参数枚举

| 参数值 | 中文名 |
|--------|--------|
| `GRADE_1` | 一年级 |
| `GRADE_2` | 二年级 |
| `GRADE_3` | 三年级 |
| `GRADE_4` | 四年级 |
| `GRADE_5` | 五年级 |
| `GRADE_6` | 六年级 |
| `GRADE_7` | 七年级 |
| `GRADE_8` | 八年级 |
| `GRADE_9` | 九年级 |
| `SENIOR_1` | 高一 |
| `SENIOR_2` | 高二 |
| `SENIOR_3` | 高三 |

## 关于"全年级"命名建议

选择框的第一个选项建议命名为 **"全校"**，比"全年级"更自然。教育管理语境下，"全校"天然涵盖所有年级。

下拉框示例：
```
┌──────────────┐
│ 全校（默认）  │  ← 各年级人数柱状图
│ 一年级        │
│ 二年级        │
│ ...          │
│ 高三          │  ← 该年级各班级人数
└──────────────┘
```

## 前端实现参考

```typescript
// 年级选项列表（从后端接口获取或写死）
const gradeOptions = [
  { value: '', label: '全校' },         // 空值 = 全校统计
  { value: 'GRADE_1', label: '一年级' },
  { value: 'GRADE_2', label: '二年级' },
  // ...
  { value: 'SENIOR_3', label: '高三' },
]

// 请求统计
async function fetchStats(grade?: string) {
  const params = grade ? { grade } : {}
  const res = await axios.get('/api/dashboard/stats/', { params })
  return {
    totals: res.data.totals,          // 四个总数
    distribution: res.data.distribution, // 年级或班级分布
    description: res.data.description,   // 图表标题
  }
}
```

## 配置位置

| 文件 | 作用 |
|------|------|
| [apps/dashboard/views.py](../apps/dashboard/views.py) | 统计接口逻辑 |
| [apps/dashboard/urls.py](../apps/dashboard/urls.py) | 路由注册 |
| [apps/dashboard/serializers.py](../apps/dashboard/serializers.py) | 响应结构文档 |
ashboard/stats
ashboard/stats
