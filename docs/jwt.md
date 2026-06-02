# JWT Token 认证

该项目从 Session 认证改为 JWT（JSON Web Token）认证。无状态、不依赖服务端存储，适合前后端分离架构。

## 核心概念

| 概念 | 说明 | 默认有效期 |
|------|------|-----------|
| **access token** | 短期访问令牌，每次 API 请求携带 | 30 分钟 |
| **refresh token** | 长期刷新令牌，access 过期后用 | 7 天 |
| **blacklist** | 黑名单表，登出或刷新后旧 token 被加入 | 持久存储 |

**安全设计**：access token 短时效（30 分钟），即使用户忘记登出，风险窗口也有限。refresh token 长时效（7 天），但每次刷新都会同时替换 refresh token（rotation），旧的即刻失效（blacklist）。

## 认证流程

```
1. 登录
   前端                           后端
   POST /api/login/ ────────────→ authenticate(username, password)
   { username, password }        ↓
                                 RefreshToken.for_user(user)
                                 ↓
   ←──────────── { user, access, refresh }

2. 访问受保护 API
   前端                           后端
   GET /api/profile/teacher/ ───→ JWTAuthentication 解析 Bearer token
   Authorization: Bearer <access> ↓
                                 request.user = 查出的用户
                                 ↓
   ←──────────── { data: {...} }

3. access token 过期后刷新
   前端                           后端
   POST /api/login/refresh/ ────→ RefreshToken(refresh)
   { refresh }                   ↓
                                 旧 refresh → 黑名单
   ←──────────── { access, refresh }   新 access + refresh

4. 登出
   前端                           后端
   POST /api/logout/ ───────────→ RefreshToken(refresh).blacklist()
   { refresh }                   ↓
   ←──────────── { message: '已退出登录' }
```

## API 端点

### POST /api/login/ — 登录

请求：
```json
{
    "username": "admin",
    "password": "123456"
}
```

成功响应：
```json
{
    "success": true,
    "code": 0,
    "message": "ok",
    "data": {
        "user": {
            "id": 1,
            "username": "admin",
            "role": "ADMIN",
            "role_display": "管理员"
        },
        "access": "eyJhbGciOi...",
        "refresh": "eyJhbGciOi..."
    },
    "meta": { "requestId": "...", "timestamp": "..." }
}
```

失败响应：
```json
{
    "success": false,
    "code": 401,
    "message": "用户名或密码错误",
    "data": { "detail": "用户名或密码错误" },
    "meta": { "requestId": "...", "timestamp": "..." }
}
```

### POST /api/login/refresh/ — 刷新 token

请求：
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
        "access": "eyJhbGciOi...",
        "refresh": "eyJhbGciOi..."
    }
}
```

### POST /api/logout/ — 登出

请求（需携带 access token 在 Authorization 头中）：
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

## 前端使用

### 1. 发送登录请求，存储 token

```typescript
async function login(username: string, password: string) {
  const res = await axios.post('/api/login/', { username, password })
  const { access, refresh } = res.data // 统一响应格式下实际在 res.data.data 中
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}
```

### 2. 配置 axios 拦截器，自动携带 token

```typescript
// 请求拦截器——自动添加 Authorization 头
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器——access 过期时自动刷新
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    // 401 且未重试过 → 尝试刷新 token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const res = await axios.post('/api/login/refresh/', { refresh })
          const { access, refresh: newRefresh } = res.data
          localStorage.setItem('access_token', access)
          localStorage.setItem('refresh_token', newRefresh)
          originalRequest.headers.Authorization = `Bearer ${access}`
          return axios(originalRequest)  // 用新 token 重试原请求
        } catch {
          // 刷新也失败 → 跳转登录页
          localStorage.clear()
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)
```

### 3. 登出

```typescript
async function logout() {
  const refresh = localStorage.getItem('refresh_token')
  await axios.post('/api/logout/', { refresh })
  localStorage.clear()
  window.location.href = '/login'
}
```

## JWT Token 结构

access token 解码后的 payload：

```json
{
    "token_type": "access",
    "exp": 1717246800,
    "iat": 1717245000,
    "jti": "abc123...",
    "user_id": 1
}
```

| 字段 | 说明 |
|------|------|
| `token_type` | `access` 或 `refresh` |
| `exp` | 过期时间（Unix 时间戳） |
| `iat` | 签发时间 |
| `jti` | Token 唯一 ID（黑名单机制依赖此字段） |
| `user_id` | 用户主键 |

## 环境变量配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | `30` | access token 有效期（分钟） |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | `7` | refresh token 有效期（天） |
| `JWT_SIGNING_KEY` | `SECRET_KEY` 的值 | JWT 签名密钥 |

## 安全注意事项

1. **access token 存储在内存中**是最安全的，localStorage 次之。不要存在 Cookie 中（避免 CSRF）
2. **access token 有效期尽量短**（当前 30 分钟），即使被窃取影响也有限
3. **refresh token 发送频率低**（仅在刷新时发送），且启用 rotation + blacklist
4. **登出只失效 refresh token**，access token 无法主动撤销——但 30 分钟后自动过期
5. **生产环境必须更换 `JWT_SIGNING_KEY`**，不要与 Django `SECRET_KEY` 共用

## 改动清单

| 文件 | 改动内容 |
|------|----------|
| `pyproject.toml` | 新增 `djangorestframework-simplejwt` 依赖 |
| `settings/base.py` | 添加 INSTALLED_APPS、REST_FRAMEWORK 认证类、SIMPLE_JWT 配置 |
| `apps/users/views.py` | LoginView 改 JWT、LogoutView 改黑名单、新增 TokenRefreshView |
| `apps/users/serializers.py` | 新增 LogoutSerializer |
| `apps/users/urls.py` | 新增 `/api/login/refresh/` 路由 |
| `.env` | 新增 JWT 环境变量 |
