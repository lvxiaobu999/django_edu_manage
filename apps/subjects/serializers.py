from rest_framework import serializers


class TotalsSerializer(serializers.Serializer):
    """总数统计序列化器"""
    teachers = serializers.IntegerField()
    students = serializers.IntegerField()
    classes = serializers.IntegerField()
    research_groups = serializers.IntegerField()


class GradeStatSerializer(serializers.Serializer):
    """年级/班级人数统计序列化器"""
    label = serializers.CharField(help_text='年级或班级名称')
    count = serializers.IntegerField(help_text='学生人数')


class DashboardStatsSerializer(serializers.Serializer):
    """仪表盘统计响应序列化器"""
    totals = TotalsSerializer()
    distribution = GradeStatSerializer(many=True)
    description = serializers.CharField(help_text='当前统计维度的描述，如"各年级人数"或"七年级各班级人数"')
