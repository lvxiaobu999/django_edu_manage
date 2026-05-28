from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.user_profile.views import (
    ResearchGroupViewSet,
    StudentProfileView,
    TeacherProfileView,
)

router = DefaultRouter()
# router.register 会自动为 ResearchGroupViewSet 生成 RESTful 路由
# prefix='research-groups' 会生成 /research-groups/、/research-groups/{id}/ 等路由
router.register('research-groups', ResearchGroupViewSet)

urlpatterns = [
    # 老师简介和学生简介不是 ViewSet，用 .as_view() 手动注册
    # TeacherProfileView 支持 POST/GET/PUT，全部映射到同一个路径
    path('teacher/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('student/', StudentProfileView.as_view(), name='student-profile'),
    # include(router.urls) 合并 router 生成的路由
    path('', include(router.urls)),
]
