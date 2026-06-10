"""学生 ViewSet —— 完整 CRUD，管理员可按 ID 操作任意学生。"""

from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsRole
from apps.core.viewsets import BaseViewSet
from apps.students.models import StudentProfile
from apps.students.serializers import StudentProfileSerializer


@extend_schema_view(
    list=extend_schema(
        summary='学生列表',
        description='管理员查看所有学生简介，支持分页。学生角色调用仅返回自己的简介。',
    ),
    create=extend_schema(
        summary='创建学生简介',
        description=(
            '为学生（或管理员为任意用户）创建一份学生简介。'
            '非管理员用户强制创建给自己，管理员可通过 `user` 字段指定目标用户。'
        ),
    ),
    retrieve=extend_schema(
        summary='查看学生详情',
        description='按 ID 查看指定学生简介。管理员可查任意学生，学生只能查自己。',
    ),
    update=extend_schema(summary='全量更新学生简介'),
    partial_update=extend_schema(summary='部分更新学生简介'),
    destroy=extend_schema(summary='删除学生简介', description='仅管理员可用。'),
)
class StudentProfileViewSet(BaseViewSet):
    queryset = StudentProfile.objects.select_related('user', 'class_id').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = StudentProfile.objects.select_related('user', 'class_id')
        if self.request.user.role == 'ADMIN':
            return qs.all()
        return qs.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ('list', 'destroy'):
            return [IsAuthenticated(), IsRole('ADMIN')()]
        return [IsAuthenticated(), IsRole(['STUDENT', 'ADMIN'])()]

    def perform_create(self, serializer):
        if self.request.user.role == 'ADMIN':
            user = serializer.validated_data.get('user', self.request.user)
        else:
            user = self.request.user
        serializer.save(user=user)
