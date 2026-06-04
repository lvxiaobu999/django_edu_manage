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

字典管理（apps.dicts）：
  path('api/', include('apps.dicts.urls'))
    → /api/subjects           → SubjectDictViewSet  (科目)
    → /api/semesters          → SemesterDictViewSet (学期)
    → /api/research-groups    → ResearchGroupDictViewSet (教研组)
    → /api/classes            → ClassDictViewSet (班级)

师生简介：
  path('api/profile/', include('apps.user_profile.urls'))
    → /api/profile/teacher  → TeacherProfileView
    → /api/profile/student  → StudentProfileView

考试管理：
  path('api/', include('apps.exam.urls'))
    → /api/exams  → ExamPlanViewSet

成绩管理：
  path('api/', include('apps.score.urls'))
    → /api/scores → ScoreViewSet

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
    path('api/', include('apps.dicts.urls')),
    path('api/profile/', include('apps.user_profile.urls')),
    path('api/', include('apps.exam.urls')),
    path('api/', include('apps.score.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
]
