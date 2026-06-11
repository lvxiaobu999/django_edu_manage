from rest_framework import serializers

from apps.core.choices import GradeChoices
from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict


class ClassSimpleSerializer(serializers.Serializer):
    """年级-班级联动接口中的班级信息。"""
    class_id = serializers.IntegerField()
    class_name = serializers.CharField()


class GradeClassesItemSerializer(serializers.Serializer):
    """年级-班级联动接口中单个年级及其班级列表。"""
    grade_id = serializers.CharField()
    grade_name = serializers.CharField()
    classes = ClassSimpleSerializer(many=True)


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
