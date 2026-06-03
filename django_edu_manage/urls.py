"""
根 URL 路由配置。

include() 的作用是将其他 urls.py 的子路由挂载到指定前缀下：
  path('api/', include('apps.users.urls'))
    → /api/register/    → RegisterView
    → /api/pending/     → PendingUserListView
    → /api/             → UserViewSet (list/create)
    → /api/{id}/        → UserViewSet (retrieve/update/destroy)
    → /api/{id}/approve/→ UserViewSet.approve()

  path('api/classes/', include('apps.classes.urls'))
    → /api/classes/         → ClassesViewSet (list/create)
    → /api/classes/{id}/    → ClassesViewSet (retrieve/update/destroy)

  path('api/profile/', include('apps.user_profile.urls'))
    → /api/profile/teacher/          → TeacherProfileView
    → /api/profile/student/          → StudentProfileView
    → /api/profile/research-groups/  → ResearchGroupViewSet
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/classes/', include('apps.classes.urls')),
    path('api/profile/', include('apps.user_profile.urls')),
    path('api/research-groups/', include('apps.research_group.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
]
