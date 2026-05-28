from rest_framework import serializers

from apps.classes.models import Classes


class ClassesSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    headmaster_name = serializers.CharField(source='headmaster.realname', read_only=True, default='')

    class Meta:
        model = Classes
        fields = [
            'id', 'grade', 'grade_display', 'name',
            'headmaster', 'headmaster_name',
        ]
