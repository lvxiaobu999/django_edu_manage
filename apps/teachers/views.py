"""教师 ViewSet —— 完整 CRUD，管理员可按 ID 操作任意教师。"""

from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsRole
from apps.core.viewsets import BaseViewSet
from apps.teachers.models import TeacherProfile
from apps.teachers.serializers import TeacherProfileSerializer


@extend_schema_view(
    list=extend_schema(
        summary='教师列表',
        description='管理员查看所有教师简介，支持分页。教师角色调用仅返回自己的简介。',
    ),
    create=extend_schema(
        summary='创建教师简介',
        description='为教师（或管理员为任意用户）创建一份教师简介。非管理员用户强制创建给自己。',
    ),
    retrieve=extend_schema(
        summary='查看教师详情',
        description='按 ID 查看指定教师简介。管理员可查任意教师，教师只能查自己。',
    ),
    update=extend_schema(summary='全量更新教师简介'),
    partial_update=extend_schema(summary='部分更新教师简介'),
    destroy=extend_schema(summary='删除教师简介', description='仅管理员可用。'),
)
class TeacherProfileViewSet(BaseViewSet):
    queryset = TeacherProfile.objects.select_related('user').all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = TeacherProfile.objects.select_related('user')
        if self.request.user.role == 'ADMIN':
            return qs.all()
        return qs.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ('list', 'destroy'):
            return [IsAuthenticated(), IsRole('ADMIN')()]
        return [IsAuthenticated(), IsRole(['TEACHER', 'ADMIN'])()]

    def perform_create(self, serializer):
        if self.request.user.role == 'ADMIN':
            user = serializer.validated_data.get('user', self.request.user)
        else:
            user = self.request.user
        serializer.save(user=user)
