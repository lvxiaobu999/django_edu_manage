"""
根 URL 路由配置。

认证端点（apps.auth）：
  path('api/', include('apps.auth.urls'))
    → POST /api/login          → LoginView
    → POST /api/logout         → LogoutView
    → POST /api/token_refresh  → TokenRefreshView
    → POST /api/register       → RegisterView

用户管理（apps.users）：
  path('api/', include('apps.users.urls'))
    → GET    /api/users            → UserViewSet.list()
    → POST   /api/users            → UserViewSet.create()
    → GET    /api/users/{id}       → UserViewSet.retrieve()
    → PUT    /api/users/{id}       → UserViewSet.update()
    → DELETE /api/users/{id}       → UserViewSet.destroy()
    → POST   /api/users/{id}/approve → UserViewSet.approve()
    → GET    /api/users/pending    → PendingUserListView

班级管理：
  path('api/', include('apps.classes.urls'))
    → GET    /api/classes           → ClassesViewSet.list()
    → POST   /api/classes           → ClassesViewSet.create()
    → GET    /api/classes/{id}      → ClassesViewSet.retrieve()
    → PUT    /api/classes/{id}      → ClassesViewSet.update()
    → DELETE /api/classes/{id}      → ClassesViewSet.destroy()

师生简介：
  path('api/profile/', include('apps.user_profile.urls'))
    → /api/profile/teacher  → TeacherProfileView
    → /api/profile/student  → StudentProfileView

教研组：
  path('api/', include('apps.research_group.urls'))
    → GET    /api/research-groups       → ResearchGroupViewSet.list()
    → POST   /api/research-groups       → ResearchGroupViewSet.create()
    → GET    /api/research-groups/{id}  → ResearchGroupViewSet.retrieve()
    → PUT    /api/research-groups/{id}  → ResearchGroupViewSet.update()
    → DELETE /api/research-groups/{id}  → ResearchGroupViewSet.destroy()

仪表盘：
  path('api/dashboard/', include('apps.dashboard.urls'))
    → GET /api/dashboard/stats
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.auth.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.classes.urls')),
    path('api/profile/', include('apps.user_profile.urls')),
    path('api/', include('apps.research_group.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
]
