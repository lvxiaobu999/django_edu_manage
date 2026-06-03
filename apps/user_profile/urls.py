# user_profile 路由：
#   /api/profile/teacher  → TeacherProfileView (POST/GET/PUT)
#   /api/profile/student  → StudentProfileView (POST/GET/PUT)

from django.urls import path

from apps.user_profile.views import StudentProfileView, TeacherProfileView

urlpatterns = [
    path('teacher', TeacherProfileView.as_view(), name='teacher-profile'),
    path('student', StudentProfileView.as_view(), name='student-profile'),
]
