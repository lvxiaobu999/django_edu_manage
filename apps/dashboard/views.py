from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.core.choices import GradeChoices
from apps.core.query_params import get_choice_param
from apps.dashboard.serializers import DashboardStatsSerializer
from apps.dicts.models import ClassDict, ResearchGroupDict
from apps.students.models import StudentProfile
from apps.teachers.models import TeacherProfile
from django_edu_manage.common.response import ok


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='仪表盘统计',
        description='返回教师/学生/班级/教研组总数及各年级人数分布。传 grade 参数可查指定年级各班级人数。',
        parameters=[
            OpenApiParameter(name='grade', description='年级编码（可选）', required=False, type=str,
                             enum=GradeChoices.values),
        ],
    )
    def get(self, request):
        # === 总数统计 ===
        # 直接从各表 count，一次 SQL 一个，简单高效
        totals = {
            'teachers': TeacherProfile.objects.count(),
            'students': StudentProfile.objects.count(),
            'classes': ClassDict.objects.count(),
            'research_groups': ResearchGroupDict.objects.count(),
        }

        # === 分布统计 ===
        # grade 是可选枚举参数，先校验再分支统计，避免无效年级编码继续执行查询。
        grade = get_choice_param(request.query_params, 'grade', GradeChoices.values)

        if grade:
            # 指定了年级 → 统计该年级下各班级的学生人数
            grade_label = dict(GradeChoices.choices)[grade]
            # 用 Classes 为主表左连 students（related_name），
            # 即使某班没有学生也能显示 count=0
            distribution = list(
                ClassDict.objects
                .filter(grade=grade)
                .annotate(count=Count('students'))
                .order_by('name')
                .values('name', 'count')
            )
            distribution = [
                {'label': item['name'], 'count': item['count']}
                for item in distribution
            ]
            description = f'{grade_label}各班级人数'
        else:
            # 未指定年级（全校）→ 统计各年级的学生人数
            # 遍历所有年级枚举，确保没有学生的年级也显示 count=0
            # 全校年级分布用一次 GROUP BY 聚合查询完成，避免每个年级单独 count() 造成多次查库。
            grade_counts = dict(
                StudentProfile.objects
                .filter(class_id__grade__isnull=False)
                .values('class_id__grade')
                .annotate(count=Count('id'))
                .values_list('class_id__grade', 'count')
            )
            distribution = []
            for value, label in GradeChoices.choices:
                # 按枚举补齐所有年级；没有学生的年级显示为 0，前端不用再补数据。
                distribution.append({'label': label, 'count': grade_counts.get(value, 0)})
            description = '各年级人数'

        data = DashboardStatsSerializer({
            'totals': totals,
            'distribution': distribution,
            'description': description,
        }).data

        return ok(data=data)
