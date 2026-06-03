# NoSlashRouter 为 ResearchGroupViewSet 自动生成路由：
#   GET    /api/research-groups       → list
#   POST   /api/research-groups       → create
#   GET    /api/research-groups/{id}  → retrieve
#   PUT    /api/research-groups/{id}  → update
#   DELETE /api/research-groups/{id}  → destroy

from django.urls import include, path

from apps.core.routers import NoSlashRouter
from apps.research_group.views import ResearchGroupViewSet

router = NoSlashRouter()
router.register('research-groups', ResearchGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
