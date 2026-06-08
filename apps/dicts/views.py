# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 NoSlashRouter 自动生成 RESTful URL。

from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import StandardResultsSetPagination
from apps.core.viewsets import BaseViewSet
from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict
from apps.dicts.serializers import (
    ClassDictSerializer,
    ResearchGroupDictSerializer,
    SemesterDictSerializer,
    SubjectDictSerializer,
)


class SubjectDictViewSet(BaseViewSet):
    queryset = SubjectDict.objects.all()
    serializer_class = SubjectDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class SemesterDictViewSet(BaseViewSet):
    queryset = SemesterDict.objects.all()
    serializer_class = SemesterDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class ResearchGroupDictViewSet(BaseViewSet):
    queryset = ResearchGroupDict.objects.all()
    serializer_class = ResearchGroupDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class ClassDictViewSet(BaseViewSet):
    # queryset = ClassDict.objects.select_related('headmaster__user')
    queryset = ClassDict.objects.all()
    serializer_class = ClassDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = ClassDict.objects.select_related('headmaster')

        grade = self.request.query_params.get('grade', '').strip()
        if grade:
            qs = qs.filter(grade=grade)

        name = self.request.query_params.get('name', '').strip()
        if name:
            qs = qs.filter(name__icontains=name)

        headmaster = self.request.query_params.get('headmaster', '').strip()
        if headmaster:
            qs = qs.filter(headmaster__realname__icontains=headmaster)

        return qs
