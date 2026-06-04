from rest_framework import serializers

from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict


class SubjectDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectDict
        fields = ['id', 'name']


class SemesterDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterDict
        fields = ['id', 'name', 'display_name']


class ResearchGroupDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroupDict
        fields = ['id', 'name']


class ClassDictSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    headmaster_name = serializers.CharField(source='headmaster.realname', read_only=True, default='')

    class Meta:
        model = ClassDict
        fields = ['id', 'grade', 'grade_display', 'name', 'headmaster', 'headmaster_name']
