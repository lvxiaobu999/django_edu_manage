"""教师 ViewSet —— 完整 CRUD，管理员可按 ID 操作任意教师。"""

from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsRole
from apps.core.query_params import get_str_param
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
    # select_related('user')：user 是一对一关系，使用 SQL JOIN 一次查出，避免访问 user 时再查库。
    # prefetch_related(...)：research_groups/class_ids 是多对多关系，批量预取可避免教师列表序列化时出现 N+1 查询。
    queryset = TeacherProfile.objects.select_related('user').prefetch_related(
        'research_groups',
        'class_ids',
    ).order_by('id')
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # 这里和 queryset 保持一致：基础查询先预加载序列化会用到的关联数据，再叠加角色和查询参数过滤。
        qs = TeacherProfile.objects.select_related('user').prefetch_related(
            'research_groups',
            'class_ids',
        )

        if self.request.user.role != 'ADMIN':
            return qs.filter(user=self.request.user).order_by('id')
        
        # 查询参数过滤
        emp_no = get_str_param(self.request.query_params, 'emp_no')
        if emp_no:
            qs = qs.filter(emp_no__icontains=emp_no)
        realname = get_str_param(self.request.query_params, 'realname')
        if realname:
            qs = qs.filter(realname__icontains=realname)


        return qs.order_by('id')

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
