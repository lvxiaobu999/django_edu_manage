from django.urls import include, path

from apps.classes.views import ClassesViewSet
from apps.core.routers import NoSlashRouter

router = NoSlashRouter()
router.register('classes', ClassesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
