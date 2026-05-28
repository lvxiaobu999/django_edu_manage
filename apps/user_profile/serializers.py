from rest_framework import serializers

from apps.user_profile.models import StudentProfile, TeacherProfile


# === 老师简介序列化器 ===
class TeacherProfileSerializer(serializers.ModelSerializer):
    # source='user.username'：跨 OneToOneField 读取关联 User 的字段
    user_name = serializers.CharField(source='user.username', read_only=True)
    # SerializerMethodField：自定义输出字段，方法名格式 get_<field_name>
    research_group_names = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'user_name', 'emp_no', 'realname',
            'phone', 'email', 'address', 'age', 'gender',
            'research_groups', 'research_group_names', 'class_ids',
        ]
        read_only_fields = ['user']  # user 由服务端自动填入

    def get_research_group_names(self, obj):
        """多对多关联的教研组名称列表，纯展示用"""
        return [g.name for g in obj.research_groups.all()]

    def validate(self, attrs):
        """对象级校验：self.instance 为 None 表示创建，否则是更新"""
        if self.instance is None:
            if TeacherProfile.objects.filter(user=self.context['request'].user).exists():
                raise serializers.ValidationError('已完善过简介')
        return attrs

    def create(self, validated_data):
        """创建时自动从 request 中取当前用户，前端不需要传 user 字段"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# === 学生简介序列化器 ===
class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    # source='class_id.name'：跨 ForeignKey 多层取值，读取班级名称
    class_name = serializers.CharField(source='class_id.name', read_only=True, default='')

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_name', 'stu_no', 'realname',
            'phone', 'email', 'address', 'age', 'gender',
            'class_id', 'class_name',
        ]
        read_only_fields = ['user']

    def validate(self, attrs):
        if self.instance is None:
            if StudentProfile.objects.filter(user=self.context['request'].user).exists():
                raise serializers.ValidationError('已完善过简介')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
