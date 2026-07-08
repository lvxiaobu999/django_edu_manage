from rest_framework import serializers

from apps.students.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_id.name', read_only=True, default='')
    grade = serializers.CharField(source='class_id.grade', read_only=True, default='')
    grade_display = serializers.CharField(source='class_id.get_grade_display', read_only=True, default='')

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_name', 'stu_no', 'realname',
            'phone', 'email', 'address', 'age', 'gender',
            'class_id', 'class_name', 'grade', 'grade_display',
        ]


class StudentImportExcelSerializer(serializers.Serializer):
    file = serializers.FileField(help_text='学生信息 Excel 文件，仅支持 .xlsx')
    default_password = serializers.CharField(
        required=False,
        allow_blank=True,
        default='z123456.',
        help_text='未在 Excel 中填写“密码/初始密码”列时使用的默认密码',
    )

    def validate_file(self, value):
        if not value.name.lower().endswith('.xlsx'):
            raise serializers.ValidationError('仅支持 .xlsx 文件')
        return value


class StudentImportErrorSerializer(serializers.Serializer):
    row = serializers.IntegerField(help_text='Excel 行号，从 1 开始')
    stu_no = serializers.CharField(help_text='学号', allow_blank=True)
    realname = serializers.CharField(help_text='姓名', allow_blank=True)
    messages = serializers.ListField(
        child=serializers.CharField(),
        help_text='该行的错误信息集合',
    )


class StudentImportResultSerializer(serializers.Serializer):
    total_rows = serializers.IntegerField(help_text='参与导入的数据行数，不包含表头和空行')
    imported_count = serializers.IntegerField(help_text='成功导入数量')
    failed_count = serializers.IntegerField(help_text='失败行数量')
    errors = StudentImportErrorSerializer(many=True, help_text='逐行错误明细')
