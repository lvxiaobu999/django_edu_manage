# DefaultRouter 为 ResearchGroupViewSet 自动生成路由：
#   GET    /                     → list
#   POST   /                     → create
#   GET    /{id}/                → retrieve
#   PUT    /{id}/                → update
#   DELETE /{id}/                → destroy
#
# 根路由中通过 path('api/research-groups/', include(...)) 挂载，
# 最终完整路径为 /api/research-groups/

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.research_group.views import ResearchGroupViewSet

router = DefaultRouter()
router.register('', ResearchGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
