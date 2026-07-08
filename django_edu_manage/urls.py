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
  path('api/students/', include('apps.students.urls'))
    → /api/students         → StudentProfileViewSet（完整 CRUD）
  path('api/teachers/', include('apps.teachers.urls'))
    → /api/teachers         → TeacherProfileViewSet（完整 CRUD）

考试管理：
  path('api/', include('apps.exam.urls'))
    → /api/exams  → ExamPlanViewSet

成绩管理：
  path('api/', include('apps.score.urls'))
    → /api/scores → ScoreViewSet

枚举值（apps.core）：
  path('api/', include('apps.core.urls'))
    → GET /api/choices          所有枚举
    → GET /api/choices?key=roles  指定枚举

仪表盘：
  path('api/dashboard/', include('apps.dashboard.urls'))
    → GET /api/dashboard/stats

AI 助手（apps.agent）：
  path('api/', include('apps.agent.urls'))
    → POST   /api/agent/chat           → 单次问答
    → POST   /api/agent/chat/session   → 带记忆的多轮对话
    → DELETE /api/agent/chat/session   → 清除会话记忆
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 文档
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # 业务接口
    path('api/', include('apps.core.urls')),
    path('api/', include('apps.auth.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.dicts.urls')),
    path('api/', include('apps.students.urls')),
    path('api/', include('apps.teachers.urls')),
    path('api/', include('apps.exam.urls')),
    path('api/', include('apps.score.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/', include('apps.agent.urls')),
]
