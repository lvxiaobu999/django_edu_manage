from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.user_profile.views import (
    ResearchGroupViewSet,
    StudentProfileView,
    TeacherProfileView,
)

router = DefaultRouter()
router.register('research-groups', ResearchGroupViewSet)

urlpatterns = [
    path('teacher/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('student/', StudentProfileView.as_view(), name='student-profile'),
    path('', include(router.urls)),
]
