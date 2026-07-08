"""学生 ViewSet —— 完整 CRUD，管理员可按 ID 操作任意学生。

查询参数（仅 list）：
    stu_no    — 学号模糊搜索（忽略大小写），如 ?stu_no=2024
    realname  — 姓名模糊搜索（忽略大小写），如 ?realname=张
    grade     — 年级编码精确匹配，如 ?grade=GRADE_1
    class_id  — 班级 ID 精确匹配，如 ?class_id=1
"""

from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.choices import GradeChoices
from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsRole
from apps.core.query_params import get_choice_param, get_int_param, get_str_param
from apps.core.viewsets import BaseViewSet
from apps.students.models import StudentProfile
from apps.students.serializers import StudentProfileSerializer


@extend_schema_view(
    list=extend_schema(
        summary='学生列表',
        description='管理员查看所有学生简介，支持按学号、姓名、年级、班级筛选并分页。'
                    '学生角色调用仅返回自己的简介。',
        parameters=[
            OpenApiParameter(name='stu_no', description='学号模糊搜索', required=False, type=str),
            OpenApiParameter(name='realname', description='姓名模糊搜索', required=False, type=str),
            OpenApiParameter(name='grade', description='年级编码精确匹配', required=False, type=str,
                             enum=GradeChoices.values),
            OpenApiParameter(name='class_id', description='班级 ID 精确匹配', required=False, type=int),
        ],
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
    # select_related 预加载用户和班级，序列化 user_name/class_name/grade 时不再额外查库。
    # order_by('id') 保证分页顺序稳定，避免数据变化时同一条记录在不同页来回跳。
    queryset = StudentProfile.objects.select_related('user', 'class_id').order_by('id')
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # 基础查询先带上关联表，后续再根据角色和查询参数逐步收窄范围。
        qs = StudentProfile.objects.select_related('user', 'class_id')

        # 角色权限过滤：管理员看全部，学生只能看自己
        if self.request.user.role != 'ADMIN':
            qs = qs.filter(user=self.request.user)

        # 查询参数过滤
        stu_no = get_str_param(self.request.query_params, 'stu_no')
        if stu_no:
            qs = qs.filter(stu_no__icontains=stu_no)

        realname = get_str_param(self.request.query_params, 'realname')
        if realname:
            qs = qs.filter(realname__icontains=realname)

        # grade 是枚举字段，先校验是否属于 GradeChoices，避免无效值直接进入查询。
        grade = get_choice_param(self.request.query_params, 'grade', GradeChoices.values)
        if grade:
            qs = qs.filter(class_id__grade=grade)

        # class_id 是数据库主键，先转成整数；非法值会返回参数错误，而不是落到数据库层。
        class_id = get_int_param(self.request.query_params, 'class_id')
        if class_id:
            qs = qs.filter(class_id_id=class_id)

        # 最终统一排序，配合分页返回稳定结果。
        return qs.order_by('id')

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
