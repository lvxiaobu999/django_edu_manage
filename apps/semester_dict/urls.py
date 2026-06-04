from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.semester_dict.views import SemesterViewSet

router = NoSlashRouter()
router.register('semesters', SemesterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
