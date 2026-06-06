# JWT Token 认证设计

## 核心概念

| 概念 | 说明 | 默认有效期 |
|------|------|-----------|
| **access token** | 短期访问令牌，每次 API 请求携带 | 30 分钟 |
| **refresh token** | 长期刷新令牌，access 过期后用来换新的 | 7 天 |
| **blacklist** | 黑名单表，登出或刷新后旧 token 被加入 | 持久存储 |

---

## 认证流程

```
1. 登录
   POST /api/login ────────────→ authenticate(username, password)
   { username, password }       ↓
                                RefreshToken.for_user(user)
                                ↓
   ←──────── { user, access, refresh }

2. 访问受保护 API
   GET /api/xxx ───────────────→ JWTAuthentication 解析 Bearer token
   Authorization: Bearer <access> ↓
                                request.user = 查出的用户
                                ↓
   ←──────── { data: {...} }

3. access token 过期后刷新
   POST /api/token_refresh ────→ 验证 refresh token
   { refresh }                  ↓
                                旧 refresh → 黑名单，生成新 JTI
   ←──────── { access, refresh }

4. 登出
   POST /api/logout ───────────→ refresh.blacklist()
   { refresh }                  ↓
   ←──────── { message: '已退出登录' }
```

---

## Refresh Token 轮转（Rotation）设计分析

### 当前行为

`ROTATE_REFRESH_TOKENS=True` + `BLACKLIST_AFTER_ROTATION=True`：

每次调用 `/api/token_refresh`，不仅换发新的 access token，**refresh token 本身也会被替换**——旧 refresh token 进入黑名单，返回一个全新的 refresh token。

### 轮转解决什么问题

```
场景：攻击者通过 XSS / 日志泄露 / 中间人 窃取了 refresh token

无轮转：
  攻击者持有 refresh token ──→ 7 天内随时刷新获取 access token ──→ 持续访问
  用户无感知，无法主动终止

有轮转：
  用户正常刷新 ──→ 旧 token 进黑名单
  攻击者用旧 token 刷新 ──→ 被拒绝（黑名单命中）
  服务端可据此检测到 token 被盗（可选）
```

轮转的核心价值是**限制泄露后的时间窗口**：攻击者必须在用户刷新之前使用偷来的 token，而且只能用一次。

### 为什么有人认为是过度设计

1. **access token 本身就是短期防护**。30 分钟有效期已经大幅限制了泄露后的影响范围。

2. **race condition 问题**：如果攻击者比合法用户先刷新，那合法用户的 token 反而被黑名单，导致合法用户被登出——攻击者拿到了新 token，防御反而伤到了自己。

3. **前端可靠性风险**：刷新是异步的，如果前端在收到响应后、写入 localStorage 前崩溃（或网络断开），新的 refresh token 丢失，用户只能重新登录。这是轮转最大的工程代价。

4. **OAuth 2.0 规范并未要求轮转**。RFC 6749 中 refresh token 是可选的，轮转更是各实现自己加的。

5. **refresh token 使用频率极低**（每 30 分钟一次），在正常网络环境下，传输中被截获的概率远低于 access token。

### 为什么本项目保留了轮转

| 理由 | 说明 |
|------|------|
| **教育项目，学习完整方案** | 了解业界最佳实践的完整形态，再根据实际需求裁剪 |
| **未来可能接入第三方** | 若后续对接微信/钉钉等 OAuth 方，rotation 是常见要求 |
| **关闭成本极低** | 两行配置即可关闭，没有代码耦合 |
| **refresh token 轮转失败只影响一次登录** | 不是数据丢失，代价可控 |

### 如何关闭轮转

如果觉得不需要，`settings/base.py` 中改两行即可：

```python
SIMPLE_JWT = {
    # ...
    'ROTATE_REFRESH_TOKENS': False,       # 改这里
    'BLACKLIST_AFTER_ROTATION': False,    # 改这里
}
```

关闭后 `/api/token_refresh` 只返回新 access token，refresh token 保持不变，前端无需每次更新存储的 refresh token。

---

## API 端点

### POST /api/login — 登录

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
    "data": {
        "user": { "id": 1, "username": "admin", "role": "ADMIN", "role_display": "管理员" },
        "access": "eyJhbGciOi...",
        "refresh": "eyJhbGciOi..."
    }
}
```

### POST /api/token_refresh — 刷新 token

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
    "data": {
        "access": "eyJhbGciOi...",
        "refresh": "eyJhbGciOi..."
    }
}
```

> 轮转开启时 `refresh` 字段每次都是新值，前端必须替换本地存储中的旧 refresh token。

### POST /api/logout — 登出

请求（需携带 access token）：
```json
{
    "refresh": "eyJhbGciOi..."
}
```

成功响应：
```json
{
    "success": true,
    "message": "已退出登录"
}
```

---

## 前端使用

### 1. 登录后存储

```typescript
async function login(username: string, password: string) {
  const res = await axios.post('/api/login', { username, password })
  const { access, refresh } = res.data.data
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}
```

### 2. 自动携带 + 过期自动刷新

```typescript
// 请求拦截器——自动添加 Authorization 头
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器——401 时自动刷新
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) {
        window.location.href = '/login'
        return Promise.reject(error)
      }
      try {
        const res = await axios.post('/api/token_refresh', { refresh })
        const { access, refresh: newRefresh } = res.data.data
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', newRefresh) // 轮转时必须替换
        originalRequest.headers.Authorization = `Bearer ${access}`
        return axios(originalRequest)
      } catch {
        localStorage.clear()
        window.location.href = '/login'
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
  await axios.post('/api/logout', { refresh }).catch(() => {})
  localStorage.clear()
  window.location.href = '/login'
}
```

---

## Token 结构

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

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | `30` | access token 有效期（分钟） |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | `7` | refresh token 有效期（天） |
| `JWT_SIGNING_KEY` | `SECRET_KEY` 的值 | JWT 签名密钥 |

---

## 安全注意事项

1. **access token 存在内存或 localStorage**，不要存在 Cookie（避免 CSRF）
2. **access token 有效期尽量短**（当前 30 分钟），即使泄露影响也有限
3. **生产环境必须更换 `JWT_SIGNING_KEY`**，不要与 Django `SECRET_KEY` 共用
4. **登出只失效 refresh token**，access token 无法主动撤销——30 分钟后自动过期
