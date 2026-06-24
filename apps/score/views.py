"""成绩 ViewSet —— 完整 CRUD，支持按考试、科目、学生、年级、班级筛选。"""

from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.choices import GradeChoices
from apps.core.pagination import StandardResultsSetPagination
from apps.core.viewsets import BaseViewSet
from apps.score.models import Score
from apps.score.serializers import ScoreSerializer


@extend_schema_view(
    list=extend_schema(
        summary='成绩列表',
        description='所有成绩记录，预加载学生/考试/科目关联信息。'
                    '支持按考试、科目、学生姓名、年级、班级筛选。',
        parameters=[
            OpenApiParameter(name='exam', description='考试 ID 精确匹配', required=False, type=int),
            OpenApiParameter(name='subject', description='科目 ID 精确匹配', required=False, type=int),
            OpenApiParameter(name='student', description='学生姓名模糊搜索', required=False, type=str),
            OpenApiParameter(name='grade', description='年级编码精确匹配', required=False, type=str,
                             enum=GradeChoices.values),
            OpenApiParameter(name='class_id', description='班级 ID 精确匹配', required=False, type=int),
        ],
    ),
    create=extend_schema(summary='录入成绩', description='新增一条成绩记录（同一学生+考试+科目不可重复）。'),
    retrieve=extend_schema(summary='查看成绩详情'),
    update=extend_schema(summary='全量更新成绩'),
    partial_update=extend_schema(summary='部分更新成绩'),
    destroy=extend_schema(summary='删除成绩'),
)
class ScoreViewSet(BaseViewSet):
    queryset = Score.objects.select_related('student', 'exam', 'subject').all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Score.objects.select_related('student', 'exam', 'subject')

        exam = self.request.query_params.get('exam', '').strip()
        if exam:
            qs = qs.filter(exam=exam)

        subject = self.request.query_params.get('subject', '').strip()
        if subject:
            qs = qs.filter(subject=subject)

        student = self.request.query_params.get('student', '').strip()
        if student:
            qs = qs.filter(student__realname__icontains=student)

        return qs