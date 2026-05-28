from rest_framework import serializers

from apps.research_group.models import ResearchGroup


# 教研组字段简单，直接用 ModelSerializer 自动生成
class ResearchGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ['id', 'name']
