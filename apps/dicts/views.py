# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 NoSlashRouter 自动生成 RESTful URL。

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict
from apps.dicts.serializers import (
    ClassDictSerializer,
    ResearchGroupDictSerializer,
    SemesterDictSerializer,
    SubjectDictSerializer,
)


class SubjectDictViewSet(viewsets.ModelViewSet):
    queryset = SubjectDict.objects.all()
    serializer_class = SubjectDictSerializer
    permission_classes = [IsAuthenticated]


class SemesterDictViewSet(viewsets.ModelViewSet):
    queryset = SemesterDict.objects.all()
    serializer_class = SemesterDictSerializer
    permission_classes = [IsAuthenticated]


class ResearchGroupDictViewSet(viewsets.ModelViewSet):
    queryset = ResearchGroupDict.objects.all()
    serializer_class = ResearchGroupDictSerializer
    permission_classes = [IsAuthenticated]


class ClassDictViewSet(viewsets.ModelViewSet):
    queryset = ClassDict.objects.select_related('headmaster__user')
    serializer_class = ClassDictSerializer
    permission_classes = [IsAuthenticated]
