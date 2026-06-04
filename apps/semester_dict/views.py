# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 NoSlashRouter 自动生成 RESTful URL。

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.semester_dict.models import Semester
from apps.semester_dict.serializers import SemesterSerializer


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]
