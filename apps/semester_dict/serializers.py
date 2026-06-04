from rest_framework import serializers

from apps.semester_dict.models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'display_name']
