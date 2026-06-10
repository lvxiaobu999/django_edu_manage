from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.teachers.views import TeacherProfileViewSet

router = NoSlashRouter()
router.register('teachers', TeacherProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
