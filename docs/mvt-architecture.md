# Django DRF 三层架构：Model / Serializer / View

## 一句话理解

```
客户端请求  →  View（调度）  →  Model（数据库）  →  Serializer（格式化）  →  客户端响应
                "做什么"          "数据在哪"            "长什么样"
```

三者各司其职，互不越界。下面用你项目里的真实代码来拆解。

---

## 一、Model —— 数据库的"图纸"

**文件位置：** [apps/classes/models.py](../apps/classes/models.py)

**职责：定义数据长什么样，存在数据库里。**

```python
class Classes(models.Model):
    grade = models.CharField(max_length=20, choices=GradeChoices.choices)
    name = models.CharField(max_length=50)
    headmaster = models.ForeignKey('teachers.TeacherProfile', ...)

    class Meta:
        db_table = 'classes'          # 数据库表名
        ordering = ['grade', 'name']   # 默认排序
        constraints = [
            models.UniqueConstraint(fields=['grade', 'name'], ...)  # 唯一约束
        ]
```

Model 只关心三件事：
| 关注点 | 例子 |
|--------|------|
| 字段类型和约束 | `CharField(max_length=50)`、`ForeignKey` |
| 数据库层配置 | 表名、索引、唯一约束、默认排序 |
| 数据完整性 | `on_delete=models.SET_NULL`（删了班主任，班级还在） |

**Model 不关心的事：**
- 请求怎么来的（那是 View 的事）
- 返回给客户端叫什么名字（那是 Serializer 的事）
- 业务逻辑（可以在 View 里，也可以抽到 Service 层）

---

## 二、Serializer —— 数据的"翻译官"

**文件位置：** [apps/classes/serializers.py](../apps/classes/serializers.py)

**职责：Model 对象 ↔ JSON 的互相转换，以及数据校验。**

### 2.1 序列化（Model → JSON，输出）

```python
class ClassesSerializer(serializers.ModelSerializer):
    # 把数据库存的 'GRADE_7' 翻译成 '七年级'
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)

    # 跨表取值：headmaster 是外键 → TeacherProfile → realname 字段
    headmaster_name = serializers.CharField(source='headmaster.realname', read_only=True)

    class Meta:
        model = Classes
        fields = ['id', 'grade', 'grade_display', 'name', 'headmaster', 'headmaster_name']
```

数据库里存的 → Serializer 翻译后返回的：

```
数据库:  { grade: "GRADE_7", name: "1班", headmaster_id: 3 }
                              ↓ Serializer
客户端:  { "grade_display": "七年级", "headmaster_name": "张三", ... }
```

### 2.2 反序列化（JSON → Model，输入/创建/更新）

Serializer 还会校验输入数据：类型对不对、必填字段有没有缺失、值是否合法。这些都由 DRF 自动处理，不需要手写。

### 2.3 没有 Model 也能用 Serializer

**文件位置：** [apps/dashboard/serializers.py](../apps/dashboard/serializers.py)

Dashboard 没有对应的数据库表（它是聚合统计），Serializer 退化为"响应格式说明书"：

```python
class DashboardStatsSerializer(serializers.Serializer):   # ← 继承 Serializer，不是 ModelSerializer
    totals = TotalsSerializer()
    distribution = GradeStatSerializer(many=True)
    description = serializers.CharField()
```

这里 Serializer 纯粹用来声明"我这个接口返回的数据结构长这样"，不做数据库映射。

---

## 三、View —— 请求的"调度中心"

**文件位置：** [apps/classes/views.py](../apps/classes/views.py)

**职责：接收请求 → 调取数据 → 交给 Serializer 格式化 → 返回响应。**

### 3.1 标准 CRUD 场景：ViewSet

```python
class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.select_related('headmaster__user')  # 指定数据源 + 优化查询
    serializer_class = ClassesSerializer                            # 指定用哪个序列化器
    permission_classes = [IsAuthenticated]                          # 权限控制
```

一个 `ModelViewSet` 自动生成 5 个接口：

| HTTP 方法 | URL | 动作 | 对应方法 |
|-----------|-----|------|----------|
| GET | `/classes/` | 列表 | `list()` |
| POST | `/classes/` | 创建 | `create()` |
| GET | `/classes/1/` | 详情 | `retrieve()` |
| PUT/PATCH | `/classes/1/` | 更新 | `update()` |
| DELETE | `/classes/1/` | 删除 | `destroy()` |

你不用写任何一行业务代码 —— Model + Serializer + ViewSet 组合直接就工作了。

### 3.2 自定义逻辑场景：APIView

**文件位置：** [apps/dashboard/views.py](../apps/dashboard/views.py)

Dashboard 不是简单 CRUD，它要做跨表聚合统计，所以用更底层的 `APIView`：

```python
class DashboardStatsView(APIView):
    def get(self, request):
        # 1. 拿数据（跨多张表聚合）
        totals = {
            'teachers': TeacherProfile.objects.count(),
            'students': StudentProfile.objects.count(),
            ...
        }
        # 2. 根据参数做不同逻辑
        grade = request.query_params.get('grade')
        if grade:
            distribution = ...  # 该年级各班级人数
        else:
            distribution = ...  # 全校各年级人数

        # 3. 手动组装返回
        return ok(data={'totals': totals, 'distribution': distribution, ...})
```

---

## 四、三者协作全景图

以你的 Classes 模块为例，一次 `GET /api/classes/` 请求的完整链路：

```
浏览器
  │  GET /api/classes/
  ▼
urls.py  匹配到 ClassesViewSet
  │
  ▼
View ─── permission_classes = [IsAuthenticated]  → 校验 JWT token
  │
  ▼
View ─── queryset = Classes.objects.select_related(...)  → 生成 SQL 查询
  │
  ▼
Database  返回 QuerySet [Classes对象1, Classes对象2, ...]
  │
  ▼
Serializer ─── 每个 Classes 对象 → ClassesSerializer 处理 →
  │              grade='GRADE_7'  →  grade_display='七年级'
  │              headmaster_id=3  →  headmaster_name='张三'
  ▼
JSON 响应  [{ "id":1, "grade":"GRADE_7", "grade_display":"七年级", ... }, ...]
```

### 谁负责什么——一句话版

| 层 | 一句话 |
|----|--------|
| **Model** | "这张表有哪些字段，字段之间什么关系" |
| **Serializer** | "数据库里的值怎么翻译成客户端能看懂的格式" |
| **View** | "这个请求应该做什么操作，调用哪些数据" |

### 常见误区

| 误区 | 正确做法 |
|------|---------|
| 在 Model 里写 API 逻辑 | Model 只描述数据结构，不碰请求/响应 |
| 在 Serializer 里写业务逻辑 | Serializer 只做转换和校验，复杂逻辑放 View 或 Service 层 |
| 在 View 里手写 JSON 拼接 | 让 Serializer 做格式化，View 只做调度 |
| 没有数据库表就不写 Serializer | Dashboard 这种场景，Serializer 退化为纯文档/校验，仍然有价值（见 [serializers.py](../apps/dashboard/serializers.py)） |

---

## 五、你的项目中的两种典型模式

### 模式 A：Model + ModelSerializer + ModelViewSet（标准 CRUD）

**代表模块：** `classes`、`users`、`students`、`teachers`、`research_group`

```
models.py        →  定义数据库表结构
serializers.py   →  ModelSerializer，声明字段映射和跨表取值
views.py         →  ModelViewSet，一行 queryset + serializer_class 搞定
```

适合：增删改查实体（班级、用户、教研组等）

### 模式 B：无 Model + Serializer + APIView（聚合/统计）

**代表模块：** `dashboard`

```
无 models.py     →  不存数据，只是查询聚合
serializers.py   →  Serializer（不是 ModelSerializer），纯声明响应结构
views.py         →  APIView，手写 get() 逻辑
```

适合：统计报表、仪表盘、跨表聚合查询
