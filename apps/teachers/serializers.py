from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.teachers.models import TeacherProfile


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    research_group_names = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_research_group_names(self, obj):
        return [g.name for g in obj.research_groups.all()]

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'user_name', 'emp_no', 'realname',
            'phone', 'email', 'address', 'age', 'gender',
            'research_groups', 'research_group_names', 'class_ids',
        ]
