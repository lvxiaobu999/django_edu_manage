# === 路由配置说明 ===
# DefaultRouter 是 DRF 提供的路由器，它能为 ViewSet 自动生成 RESTful 路由：
#   router.register('users', UserViewSet) 会生成：
#     GET    /users/       → UserViewSet.list()
#     POST   /users/       → UserViewSet.create()
#     GET    /users/{id}/  → UserViewSet.retrieve()
#     PUT    /users/{id}/  → UserViewSet.update()
#     DELETE /users/{id}/  → UserViewSet.destroy()
#     POST   /users/{id}/approve/  → UserViewSet.approve()  (来自 @action)
#
# 对于 RegisterView 和 PendingUserListView 这种非 ViewSet 视图，
# 需要手动写在 urlpatterns 里。
#
# JWT 认证端点：
#   POST /api/login/          → 提交 username + password，返回 access + refresh token
#   POST /api/logout/         → 提交 refresh token，将其加入黑名单
#   POST /api/login/refresh/  → 提交 refresh token，获取新的 access + refresh token

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    LoginView,
    LogoutView,
    PendingUserListView,
    RegisterView,
    TokenRefreshView,
    UserViewSet,
)

router = DefaultRouter()
# 注册到 router 时 prefix=''，因为用户 API 直接挂在 /api/ 下（由根 urls.py 的 include 决定）
router.register('', UserViewSet)

urlpatterns = [
    # === JWT 认证端点 ===
    # 登录：POST /api/login/  返回 { user, access, refresh }
    path('login/', LoginView.as_view(), name='login'),
    path('login', LoginView.as_view(), name='login-noslash'),

    # 登出：POST /api/logout/  将 refresh token 加入黑名单
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout', LogoutView.as_view(), name='logout-noslash'),

    # 刷新 token：POST /api/login/refresh/  用 refresh token 换取新的 access + refresh
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('login/refresh', TokenRefreshView.as_view(), name='token-refresh-noslash'),

    # === 用户管理端点 ===
    path('register/', RegisterView.as_view(), name='register'),
    path('register', RegisterView.as_view(), name='register-noslash'),
    path('pending/', PendingUserListView.as_view(), name='pending-users'),
    path('pending', PendingUserListView.as_view(), name='pending-users-noslash'),

    # include(router.urls)：将 router 生成的所有路由合并进来
    # 注意：path() 的匹配顺序很重要，Django 从上到下匹配，先匹配到的先处理
    # 所以 login/register/pending 要放在 router.urls 前面，否则会被 ViewSet 的 {id} 捕获
    path('', include(router.urls)),
]
