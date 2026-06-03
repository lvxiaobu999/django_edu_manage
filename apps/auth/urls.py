# auth 模块路由：
#   POST /api/login/          → LoginView        提交 username + password，返回 access + refresh token
#   POST /api/logout/         → LogoutView       提交 refresh token，将其加入黑名单
#   POST /api/login/refresh/  → TokenRefreshView 提交 refresh token，获取新的 access + refresh token
#   POST /api/register/       → RegisterView     提交 username + password + email + role，注册新用户

from django.urls import path

from apps.auth.views import (
    LoginView,
    LogoutView,
    RegisterView,
    TokenRefreshView,
)

urlpatterns = [
    # === JWT 认证端点 ===
    path('login/', LoginView.as_view(), name='login'),
    path('login', LoginView.as_view(), name='login-noslash'),

    # 登出
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout', LogoutView.as_view(), name='logout-noslash'),

    # 刷新 token
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('login/refresh', TokenRefreshView.as_view(), name='token-refresh-noslash'),

    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    path('register', RegisterView.as_view(), name='register-noslash'),
]
