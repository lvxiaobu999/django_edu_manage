from rest_framework import serializers

from apps.exam.models import ExamPlan


class ExamPlanSerializer(serializers.ModelSerializer):
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    semester_display = serializers.CharField(source='semester.display_name', read_only=True)

    class Meta:
        model = ExamPlan
        fields = [
            'id', 'name', 'exam_type', 'exam_type_display',
            'exam_date', 'grade', 'grade_display',
            'semester', 'semester_display',
        ]
        read_only_fields = ['name']
