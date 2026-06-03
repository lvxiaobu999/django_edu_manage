# users 模块路由：
#   GET    /api/users/            → UserViewSet.list()
#   POST   /api/users/            → UserViewSet.create()
#   GET    /api/users/{id}/       → UserViewSet.retrieve()
#   PUT    /api/users/{id}/       → UserViewSet.update()
#   DELETE /api/users/{id}/       → UserViewSet.destroy()
#   POST   /api/users/{id}/approve/ → UserViewSet.approve()
#   GET    /api/users/pending        → PendingUserListView（待审核用户列表）
#
# 认证相关端点（login/logout/register/refresh）已迁移到 apps.auth.urls

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import PendingUserListView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('users/pending', PendingUserListView.as_view(), name='pending-users'),
    path('', include(router.urls)),
]
