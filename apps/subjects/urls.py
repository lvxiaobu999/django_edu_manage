from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.subjects.views import SubjectsViewSet

router = NoSlashRouter()
router.register('subjects', SubjectsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
