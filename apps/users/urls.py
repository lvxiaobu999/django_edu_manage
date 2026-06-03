# users 模块路由：
#   GET    /api/users            → UserViewSet.list()
#   POST   /api/users            → UserViewSet.create()
#   GET    /api/users/{id}       → UserViewSet.retrieve()
#   PUT    /api/users/{id}       → UserViewSet.update()
#   DELETE /api/users/{id}       → UserViewSet.destroy()
#   POST   /api/users/{id}/approve → UserViewSet.approve()
#   GET    /api/users/pending    → PendingUserListView（待审核用户列表）

from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.users.views import PendingUserListView, UserViewSet

router = NoSlashRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('users/pending', PendingUserListView.as_view(), name='pending-users'),
    path('', include(router.urls)),
]
