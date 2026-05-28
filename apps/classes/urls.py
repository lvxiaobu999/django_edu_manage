from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.classes.views import ClassesViewSet

router = DefaultRouter()
router.register('', ClassesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
