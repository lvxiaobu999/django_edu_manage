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

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import PendingUserListView, RegisterView, UserViewSet

router = DefaultRouter()
# 注册到 router 时 prefix=''，因为用户 API 直接挂在 /api/ 下（由根 urls.py 的 include 决定）
router.register('', UserViewSet)

urlpatterns = [
    # path() 三个参数：路由规则、视图、名称（供 reverse() 反向解析）
    path('register/', RegisterView.as_view(), name='register'),
    path('pending/', PendingUserListView.as_view(), name='pending-users'),
    # include(router.urls)：将 router 生成的所有路由合并进来
    # 注意：path() 的匹配顺序很重要，Django 从上到下匹配，先匹配到的先处理
    # 所以 register/ 和 pending/ 要放在 router.urls 前面，否则会被 ViewSet 的 {id} 捕获
    path('', include(router.urls)),
]
