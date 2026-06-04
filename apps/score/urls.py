from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.score.views import ScoreViewSet

router = NoSlashRouter()
router.register('scores', ScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
