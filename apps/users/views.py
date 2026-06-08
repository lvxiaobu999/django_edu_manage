import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.pagination import StandardResultsSetPagination
from apps.core.viewsets import BaseViewSet
from apps.users.permissions import IsApprovedAdmin
from apps.users.serializers import UserSerializer
from django_edu_manage.common.response import fail, ok

User = get_user_model()
logger = logging.getLogger(__name__)


# === 待审核用户列表 ===
class PendingUserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsApprovedAdmin]

    def get_queryset(self):
        return User.objects.filter(is_approved=False)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ok(data=response.data)


# === 用户 ViewSet ===
# ModelViewSet 提供 list/create/retrieve/update/destroy 五个标准动作，
# 配合 DefaultRouter 自动生成 RESTful 路由
class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsApprovedAdmin]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = self.get_object()
        if user.is_approved:
            return fail(message='该用户已审核通过', code=400,
                        status_code=status.HTTP_400_BAD_REQUEST)
        user.is_approved = True
        user.is_active = True
        user.save()
        logger.info('管理员审核用户通过: user_id=%s, admin_id=%s', user.id, request.user.id)
        return ok(data=self.get_serializer(user).data)
