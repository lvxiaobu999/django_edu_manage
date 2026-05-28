from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import PendingUserListView, RegisterView, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('pending/', PendingUserListView.as_view(), name='pending-users'),
    path('', include(router.urls)),
]
