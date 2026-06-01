# 统一响应格式

所有 API 响应都遵循统一格式，前端无需针对不同接口做不同解析。

## 响应结构

```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {},
    "meta": {
        "requestId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "timestamp": "2025-06-01T12:00:00+00:00"
    }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | `true` 表示业务成功，`false` 表示失败 |
| `code` | number | 0 表示成功，非 0 表示错误码（HTTP 状态码） |
| `message` | string | 人类可读的提示信息 |
| `data` | any | 实际业务数据，成功时有值，失败时为错误详情 |
| `meta.requestId` | string | 唯一请求 ID，贯穿整个请求生命周期 |
| `meta.timestamp` | string | 响应时间戳（ISO 8601 UTC） |

## 成功响应示例

```bash
# GET /api/profile/teacher/
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {
        "id": 1,
        "name": "张老师",
        "phone": "13800000000"
    },
    "meta": {
        "requestId": "abc-123",
        "timestamp": "2025-06-01T12:00:00+00:00"
    }
}
```

## 失败响应示例

```bash
# POST /api/login/  （错误的密码）
{
    "success": false,
    "code": 401,
    "message": "用户名或密码错误",
    "data": {
        "detail": "用户名或密码错误"
    },
    "meta": {
        "requestId": "def-456",
        "timestamp": "2025-06-01T12:01:00+00:00"
    }
}
```

## 实现架构

整个统一响应由四层协作完成：

```
请求 → RequestIdMiddleware → DRF 视图 → UnifiedJSONRenderer → 响应（统一格式）
                                    ↓（异常）
                              unified_exception_handler → 响应（统一格式）
```

### 1. RequestIdMiddleware（`django_edu_manage/middleware.py`）

每个请求到达时生成 UUID，挂载到 `request.request_id`。后续渲染器和异常处理器读取它写入响应。

### 2. UnifiedJSONRenderer（`django_edu_manage/common/renderer.py`）

DRF 自定义 JSON 渲染器，在序列化阶段自动包裹成功响应：
- 如果视图返回的数据已经是统一格式（包含 `success`/`code`/`meta` 字段），跳过包裹
- 如果返回 `None`（如 204 No Content），跳过包裹
- 其余情况自动包裹为统一格式

只影响 JSON 格式的 DRF 响应，Browsable API 不受影响。

### 3. unified_exception_handler（`django_edu_manage/common/exceptions.py`）

DRF 自定义异常处理器，捕获所有 DRF 抛出的异常（校验失败、权限不足、404 等），转为统一格式。

### 4. ApiResponse 类（`django_edu_manage/common/response.py`）

如果视图需要精确控制响应（如手动返回失败），可以直接使用：

```python
from django_edu_manage.common.response import ApiResponse, ok, fail

# 方式一：ApiResponse
return ApiResponse(data={'id': 1}, message='创建成功')
return ApiResponse(code=1001, message='该用户已审核通过', success=False)

# 方式二：快捷函数
return ok(data={'id': 1})
return fail(message='操作失败', code=1001)
```

## 前端使用建议

```typescript
// 定义统一的响应类型
interface ApiResponse<T = any> {
  success: boolean
  code: number
  message: string
  data: T
  meta: {
    requestId: string
    timestamp: string
  }
}

// axios 拦截器中统一处理
axios.interceptors.response.use(
  (response) => {
    const body: ApiResponse = response.data
    if (!body.success) {
      // 显示错误提示
      ElMessage.error(body.message)
      return Promise.reject(body)
    }
    // 业务层只需要关心 data
    return body.data
  },
  (error) => {
    // 网络错误等非业务异常
    ElMessage.error('网络异常，请稍后重试')
    return Promise.reject(error)
  }
)
```

## 配置位置

- 中间件注册：[settings/base.py](../django_edu_manage/settings/base.py) `MIDDLEWARE` 列表末尾
- DRF 渲染器和异常处理器：[settings/base.py](../django_edu_manage/settings/base.py) `REST_FRAMEWORK` 字典
