from rest_framework import serializers

from apps.subjects.models import Subjects


class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['id', 'name']
