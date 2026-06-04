# 认证模块文档

## 概述

`apps/auth` 模块负责用户认证相关的全部功能：注册、登录、登出、Token 刷新。该模块从 `apps/users` 中独立出来，与用户管理的 CRUD 操作解耦。

**模块位置：** [apps/auth/](../apps/auth/)

## API 端点

| 方法 | URL | 说明 | 需要登录 |
|------|-----|------|---------|
| POST | `/api/login` | 登录，返回 access + refresh token | 否 |
| POST | `/api/logout` | 登出，将 refresh token 加入黑名单 | 是 |
| POST | `/api/login/refresh` | 刷新 access token | 否 |
| POST | `/api/register` | 注册新用户 | 否 |

---

## 接口详情

### 1. 登录 `POST /api/login`

请求体：

```json
{
    "username": "admin01",
    "password": "admin123"
}
```

成功响应（HTTP 200）：

```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {
        "user": {
            "id": 1,
            "username": "admin01",
            "email": "admin@school.edu.cn",
            "role": "ADMIN",
            "role_display": "管理员",
            "real_name": "",
            "is_approved": true,
            "is_active": true,
            "date_joined": "2025-01-01T00:00:00Z"
        },
        "access": "eyJhbGciOi...",
        "refresh": "eyJhbGciOi..."
    }
}
```

失败响应：

| 场景 | code | message |
|------|------|---------|
| 用户名或密码错误 | 1 | 用户名或密码错误 |
| 账户未激活 | 1 | 账户未激活，请等待管理员审核 |

### 2. 登出 `POST /api/logout`

需要携带 `Authorization: Bearer <access_token>` 头。

请求体：

```json
{
    "refresh": "eyJhbGciOi..."
}
```

成功响应：

```json
{
    "success": true,
    "code": 0,
    "message": "已退出登录",
    "data": null
}
```

> **注意：** refresh token 加入黑名单后无法再用于刷新。access token 无法主动失效，需等待自然过期（默认 30 分钟）。

### 3. 刷新 Token `POST /api/login/refresh`

access token 过期后，前端收到 HTTP 401，自动调用此接口换新 token。

请求体：

```json
{
    "refresh": "eyJhbGciOi..."
}
```

成功响应：

```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {
        "access": "eyJhbGciOi...（新的）",
        "refresh": "eyJhbGciOi...（新的）"
    }
}
```

失败响应：

| 场景 | HTTP 状态码 | message |
|------|------------|---------|
| refresh token 为空 | 400 | refresh token 不能为空 |
| token 无效或已过期 | 401 | token 无效或已过期（需重新登录） |

### 4. 注册 `POST /api/register`

请求体：

```json
{
    "username": "zhangsan",
    "password": "123456",
    "email": "zhangsan@school.edu.cn",
    "role": "STUDENT"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `username` | string | 是 | 用户名，最长 150 |
| `password` | string | 是 | 密码，最少 6 位 |
| `email` | string | 否 | 邮箱 |
| `role` | string | 是 | 角色：`ADMIN` / `TEACHER` / `STUDENT` |

成功响应（HTTP 200）：

```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {
        "id": 2,
        "username": "zhangsan",
        "email": "zhangsan@school.edu.cn",
        "role": "STUDENT",
        "role_display": "学生",
        "is_approved": false,
        "is_active": false
    }
}
```

> **注意：** 注册后 `is_active=False`、`is_approved=False`，不能登录。需管理员调用 `POST /api/users/{id}/approve` 审核通过。

---

## Token 生命周期

```
注册 → 管理员审核 → 用户登录
                        │
                        ├→ access token (默认 30 分钟有效)
                        │    └→ 过期 → 前端收到 401 → 调用 refresh 接口
                        │
                        └→ refresh token (默认 7 天有效)
                             ├→ 刷新成功 → 新 access + 新 refresh（旧的加入黑名单）
                             ├→ 用户登出 → 加入黑名单
                             └→ 过期 → 需要重新登录
```

**环境变量控制：**

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | 30 | access token 有效期（分钟） |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | 7 | refresh token 有效期（天） |

---

## 安全设计决策

| 决策 | 原因 |
|------|------|
| 登录失败返回 HTTP 200 而非 401 | 前端约定 401 仅用于 token 过期 → 重定向登录页。账号密码错误是业务错误，走 body.code 区分 |
| 注册后不自动激活 | 防止恶意注册，需管理员审核（`is_approved=True`）后才能登录 |
| access token 不可主动失效 | JWT 固有限制，缓解措施是设短有效期（30 分钟），风险窗口可控 |
| refresh token 轮转 | `ROTATE_REFRESH_TOKENS=True`，每次刷新发放新 token，旧的加入黑名单 |

---

## 前端集成示例

```typescript
// 请求拦截器：自动携带 token
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// 响应拦截器：401 自动刷新 token
axios.interceptors.response.use(
    response => response,
    async error => {
        if (error.response?.status === 401) {
            const refresh = localStorage.getItem('refresh_token')
            const { data } = await axios.post('/api/login/refresh', { refresh })
            localStorage.setItem('access_token', data.data.access)
            localStorage.setItem('refresh_token', data.data.refresh)
            // 重试原请求
            error.config.headers.Authorization = `Bearer ${data.data.access}`
            return axios(error.config)
        }
        return Promise.reject(error)
    }
)
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| [apps/auth/views.py](../apps/auth/views.py) | 登录、登出、刷新、注册视图 |
| [apps/auth/serializers.py](../apps/auth/serializers.py) | Login/Logout/Register Serializer |
| [apps/auth/urls.py](../apps/auth/urls.py) | 认证端点路由 |
| [apps/auth/apps.py](../apps/auth/apps.py) | Django App 注册 |
| [django_edu_manage/settings/base.py](../django_edu_manage/settings/base.py) | JWT 配置（`SIMPLE_JWT`） |
| [docs/permissions_auth.md](permissions_auth.md) | Django 认证与权限系统详解 |
