# user_profile 路由：
#   /api/profile/teacher/  → TeacherProfileView (POST/GET/PUT)
#   /api/profile/student/  → StudentProfileView (POST/GET/PUT)
#
# 这两个视图不是 ViewSet，而是组合了 CreateAPIView + RetrieveUpdateAPIView，
# 所以不能用 DefaultRouter 自动注册，必须手动 path() 声明

from django.urls import path

from apps.user_profile.views import StudentProfileView, TeacherProfileView

urlpatterns = [
    path('teacher/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('student/', StudentProfileView.as_view(), name='student-profile'),
]
