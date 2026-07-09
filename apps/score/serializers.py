from rest_framework import serializers

from apps.score.models import Score


class ScoreSerializer(serializers.ModelSerializer):
    # 只读的展示字段，避免前端需要额外查关联表
    student_name = serializers.CharField(source='student.realname', read_only=True)
    student_no = serializers.CharField(source='student.stu_no', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    exam_name = serializers.CharField(source='exam.name', read_only=True)

    class Meta:
        model = Score
        fields = [
            'id', 'student', 'student_name', 'student_no',
            'exam', 'exam_name', 'subject', 'subject_name',
            'score',
        ]


class ScoreImportExcelSerializer(serializers.Serializer):
    file = serializers.FileField(help_text='学生成绩 Excel 文件，仅支持 .xlsx')
    overwrite = serializers.BooleanField(
        required=False,
        default=False,
        help_text='成绩已存在时是否覆盖更新；默认 false 表示遇到重复成绩时报错',
    )

    def validate_file(self, value):
        if not value.name.lower().endswith('.xlsx'):
            raise serializers.ValidationError('仅支持 .xlsx 文件')
        return value


class ScoreImportErrorSerializer(serializers.Serializer):
    row = serializers.IntegerField(help_text='Excel 行号，从 1 开始')
    stu_no = serializers.CharField(help_text='学号', allow_blank=True)
    realname = serializers.CharField(help_text='姓名', allow_blank=True)
    messages = serializers.ListField(
        child=serializers.CharField(),
        help_text='该行的错误信息集合',
    )


class ScoreImportResultSerializer(serializers.Serializer):
    total_rows = serializers.IntegerField(help_text='参与导入的数据行数，不包含表头和空行')
    imported_count = serializers.IntegerField(help_text='新增成绩数量')
    updated_count = serializers.IntegerField(help_text='覆盖更新成绩数量')
    failed_count = serializers.IntegerField(help_text='失败行数量')
    errors = ScoreImportErrorSerializer(many=True, help_text='逐行错误明细')
