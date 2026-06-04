# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 NoSlashRouter 自动生成 RESTful URL。

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.exam.models import ExamPlan
from apps.exam.serializers import ExamPlanSerializer


class ExamPlanViewSet(viewsets.ModelViewSet):
    queryset = ExamPlan.objects.all()
    serializer_class = ExamPlanSerializer
    permission_classes = [IsAuthenticated]
