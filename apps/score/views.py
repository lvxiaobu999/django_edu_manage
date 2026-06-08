# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 NoSlashRouter 自动生成 RESTful URL。
# select_related 预加载 student/exam/subject 关联对象，避免 N+1 查询。

from rest_framework.permissions import IsAuthenticated

from apps.core.viewsets import BaseViewSet
from apps.score.models import Score
from apps.score.serializers import ScoreSerializer


class ScoreViewSet(BaseViewSet):
    queryset = Score.objects.select_related('student', 'exam', 'subject').all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
