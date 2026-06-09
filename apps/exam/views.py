# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 NoSlashRouter 自动生成 RESTful URL。

from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import StandardResultsSetPagination
from apps.core.viewsets import BaseViewSet
from apps.exam.models import ExamPlan
from apps.exam.serializers import ExamPlanSerializer


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