from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.exam.views import ExamPlanViewSet

router = NoSlashRouter()
router.register('exams', ExamPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
