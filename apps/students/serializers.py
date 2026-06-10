from rest_framework import serializers

from apps.students.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_id.name', read_only=True, default='')

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_name', 'stu_no', 'realname',
            'phone', 'email', 'address', 'age', 'gender',
            'class_id', 'class_name',
        ]
