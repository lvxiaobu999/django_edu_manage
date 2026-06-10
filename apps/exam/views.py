from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.pagination import StandardResultsSetPagination
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
    queryset = ExamPlan.objects.all()
    serializer_class = ExamPlanSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = ExamPlan.objects.select_related('semester')

        exam_type = self.request.query_params.get('exam_type', '').strip()
        if exam_type:
            qs = qs.filter(exam_type=exam_type)

        grade = self.request.query_params.get('grade', '').strip()
        if grade:
            qs = qs.filter(grade=grade)

        semester = self.request.query_params.get('semester', '').strip()
        if semester:
            qs = qs.filter(semester_id=semester)

        return qs