from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.students.views import StudentProfileViewSet

router = NoSlashRouter()
router.register('students', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
