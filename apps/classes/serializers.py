from rest_framework import serializers

from apps.classes.models import Classes


class ClassesSerializer(serializers.ModelSerializer):
    # source='get_grade_display'：DRF 会调用模型的 get_grade_display() 方法，
    # 把 'GRADE_7' 转换为 '七年级' 展示在 API 响应中
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)

    # 跨表取值：source='headmaster.realname'
    #   headmaster 是 ForeignKey → TeacherProfile 对象
    #   .realname 是 TeacherProfile 的字段
    #   DRF 自动处理关联查询（使用 select_related 优化，见 views.py）
    headmaster_name = serializers.CharField(source='headmaster.realname', read_only=True, default='')

    class Meta:
        model = Classes
        fields = [
            'id', 'grade', 'grade_display', 'name',
            'headmaster', 'headmaster_name',
        ]
