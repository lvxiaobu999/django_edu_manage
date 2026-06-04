from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.dicts.views import (
    ClassDictViewSet,
    ResearchGroupDictViewSet,
    SemesterDictViewSet,
    SubjectDictViewSet,
)

router = NoSlashRouter()
router.register('subjects', SubjectDictViewSet)
router.register('semesters', SemesterDictViewSet)
router.register('research-groups', ResearchGroupDictViewSet)
router.register('classes', ClassDictViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
