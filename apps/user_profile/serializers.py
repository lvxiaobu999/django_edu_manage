from rest_framework import serializers

from apps.user_profile.models import ResearchGroup, StudentProfile, TeacherProfile


class ResearchGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ['id', 'name']


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    research_group_names = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'user_name', 'emp_no', 'realname',
            'phone', 'email', 'address', 'research_groups',
            'research_group_names', 'class_ids',
        ]
        read_only_fields = ['user']

    def get_research_group_names(self, obj):
        return [g.name for g in obj.research_groups.all()]

    def validate(self, attrs):
        request = self.context['request']
        if self.instance is None:
            user = request.user
            if TeacherProfile.objects.filter(user=user).exists():
                raise serializers.ValidationError('已完善过简介')
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_id.name', read_only=True, default='')

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_name', 'stu_no', 'realname',
            'phone', 'email', 'address', 'class_id', 'class_name',
        ]
        read_only_fields = ['user']

    def validate(self, attrs):
        request = self.context['request']
        if self.instance is None:
            user = request.user
            if StudentProfile.objects.filter(user=user).exists():
                raise serializers.ValidationError('已完善过简介')
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
