from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.classes.views import ClassesViewSet

# DefaultRouter 自动为 ClassesViewSet 生成 RESTful 路由
router = DefaultRouter()
router.register('', ClassesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
