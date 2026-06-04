# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 DefaultRouter 自动生成 RESTful URL

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.subjects.models import Subjects
from apps.subjects.serializers import SubjectsSerializer


class SubjectsViewSet(viewsets.ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer
    permission_classes = [IsAuthenticated]
