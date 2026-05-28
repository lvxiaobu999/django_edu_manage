from rest_framework import serializers

from apps.user_profile.models import ResearchGroup, StudentProfile, TeacherProfile


class ResearchGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ['id', 'name']


# === 老师简介序列化器 ===
class TeacherProfileSerializer(serializers.ModelSerializer):
    # 通过 source='user.username' 跨表读取用户的用户名，展示给前端
    user_name = serializers.CharField(source='user.username', read_only=True)

    # SerializerMethodField：自定义方法字段，调用 get_<field_name>() 方法
    # 比 source 更灵活，可以写复杂逻辑
    research_group_names = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'user_name', 'emp_no', 'realname',
            'phone', 'email', 'address', 'research_groups',
            'research_group_names', 'class_ids',
        ]
        # user 由服务端从 request.user 自动填入，前端不需要传
        read_only_fields = ['user']

    def get_research_group_names(self, obj):
        # obj 是 TeacherProfile 实例
        # obj.research_groups.all() 返回关联的 ResearchGroup 列表
        # 用列表推导式提取 name 字段，返回教研组的名称列表
        return [g.name for g in obj.research_groups.all()]

    # 对象级校验：在所有字段级校验通过后调用
    def validate(self, attrs):
        # self.context['request'] 是 DRF 自动注入的当前请求对象
        request = self.context['request']

        # self.instance 在创建时为 None，更新时为已存在的对象
        # 这样可以在创建时检查是否已存在简介（防止重复创建）
        if self.instance is None:
            if TeacherProfile.objects.filter(user=request.user).exists():
                raise serializers.ValidationError('已完善过简介')
        return attrs

    # 覆写 create：自动将当前登录用户设为 profile 的 user
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# === 学生简介序列化器 ===
# 结构同 TeacherProfileSerializer，差异在于字段不同
class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    # source='class_id.name'：跨外键读取班级名称
    class_name = serializers.CharField(source='class_id.name', read_only=True, default='')

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_name', 'stu_no', 'realname',
            'phone', 'email', 'address', 'class_id', 'class_name',
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
