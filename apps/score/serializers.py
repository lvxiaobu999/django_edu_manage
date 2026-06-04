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
