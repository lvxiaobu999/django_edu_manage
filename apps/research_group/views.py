# ModelViewSet 一次性提供 list/create/retrieve/update/destroy 五个接口，
# 配合 DefaultRouter 自动生成 RESTful URL

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.research_group.models import ResearchGroup
from apps.research_group.serializers import ResearchGroupSerializer


class ResearchGroupViewSet(viewsets.ModelViewSet):
    queryset = ResearchGroup.objects.all()
    serializer_class = ResearchGroupSerializer
    permission_classes = [IsAuthenticated]
