import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.pagination import StandardResultsSetPagination
from apps.core.viewsets import BaseViewSet
from apps.users.permissions import IsApprovedAdmin
from apps.users.serializers import UserSerializer
from django_edu_manage.common.response import fail, ok

User = get_user_model()
logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary='未审核用户列表', description='返回所有 is_approved=False 的用户。仅已审核管理员可用。'),
)
class PendingUserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsApprovedAdmin]

    def get_queryset(self):
        # 待审核列表按 id 稳定排序，分页时结果顺序更可预期。
        return User.objects.filter(is_approved=False).order_by('id')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ok(data=response.data)


@extend_schema_view(
    list=extend_schema(summary='用户列表', description='查看所有用户，支持分页。仅已审核管理员可用。'),
    create=extend_schema(summary='创建用户'),
    retrieve=extend_schema(summary='查看用户详情'),
    update=extend_schema(summary='全量更新用户'),
    partial_update=extend_schema(summary='部分更新用户'),
    destroy=extend_schema(summary='删除用户'),
)
class UserViewSet(BaseViewSet):
    # 用户列表按 id 稳定排序，避免分页数据在默认数据库顺序下出现抖动。
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsApprovedAdmin]
    pagination_class = StandardResultsSetPagination

    @extend_schema(summary='审核用户', description='管理员审核通过指定用户（设置 is_approved=True, is_active=True）。')
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = self.get_object()
        if user.is_approved:
            return fail(message='该用户已审核通过', code=400,
                        status_code=status.HTTP_400_BAD_REQUEST)
        user.is_approved = True
        user.is_active = True
        # 这里只更新审核相关字段，避免 save() 把 username/email/role 等无关字段也写回数据库。
        user.save(update_fields=['is_approved', 'is_active'])
        logger.info('管理员审核用户通过: user_id=%s, admin_id=%s', user.id, request.user.id)
        return ok(data=self.get_serializer(user).data)
