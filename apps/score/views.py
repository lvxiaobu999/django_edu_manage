from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.viewsets import BaseViewSet
from apps.score.models import Score
from apps.score.serializers import ScoreSerializer


@extend_schema_view(
    list=extend_schema(summary='成绩列表', description='所有成绩记录，预加载学生/考试/科目关联信息。'),
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
