from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.choices import ExamTypeChoices, GradeChoices
from apps.core.pagination import StandardResultsSetPagination
from apps.core.query_params import get_choice_param, get_int_param
from apps.core.viewsets import BaseViewSet
from apps.exam.models import ExamPlan
from apps.exam.serializers import ExamPlanSerializer


@extend_schema_view(
    list=extend_schema(
        summary='考试列表',
        description='按考试类型、年级、学期筛选考试计划。',
        parameters=[
            OpenApiParameter(name='exam_type', description='考试类型', required=False, type=str,
                             enum=['MONTHLY', 'MOCK', 'MIDTERM', 'FINAL']),
            OpenApiParameter(name='grade', description='年级编码', required=False, type=str,
                             enum=['GRADE_1','GRADE_2','GRADE_3','GRADE_4','GRADE_5','GRADE_6',
                                   'GRADE_7','GRADE_8','GRADE_9','SENIOR_1','SENIOR_2','SENIOR_3']),
            OpenApiParameter(name='semester', description='学期 ID', required=False, type=int),
        ],
    ),
    create=extend_schema(summary='新增考试'),
    retrieve=extend_schema(summary='查看考试详情'),
    update=extend_schema(summary='全量更新考试'),
    partial_update=extend_schema(summary='部分更新考试'),
    destroy=extend_schema(summary='删除考试'),
)
class ExamPlanViewSet(BaseViewSet):
    # semester 是外键，select_related 可一次 JOIN 查出学期展示字段，避免序列化时再查库。
    # 按考试日期倒序 + id 排序，让列表和分页结果稳定、符合“最近考试优先”的阅读习惯。
    queryset = ExamPlan.objects.select_related('semester').order_by('-exam_date', 'id')
    serializer_class = ExamPlanSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # 列表查询同样预加载 semester，后续按考试类型、年级、学期逐步过滤。
        qs = ExamPlan.objects.select_related('semester')

        # exam_type/grade 都是枚举值，先校验再过滤，避免无效参数悄悄返回空结果或造成异常。
        exam_type = get_choice_param(self.request.query_params, 'exam_type', ExamTypeChoices.values)
        if exam_type:
            qs = qs.filter(exam_type=exam_type)

        grade = get_choice_param(self.request.query_params, 'grade', GradeChoices.values)
        if grade:
            qs = qs.filter(grade=grade)

        # semester 是外键 ID，先转整数，非法输入会走统一异常响应。
        semester = get_int_param(self.request.query_params, 'semester')
        if semester:
            qs = qs.filter(semester_id=semester)

        # 统一排序，保证分页时每次请求的顺序一致。
        return qs.order_by('-exam_date', 'id')
