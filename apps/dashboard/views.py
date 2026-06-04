from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.dashboard.serializers import DashboardStatsSerializer
from apps.dicts.models import ClassDict, GradeChoices, ResearchGroupDict
from apps.user_profile.models import StudentProfile, TeacherProfile
from django_edu_manage.common.response import fail, ok


class DashboardStatsView(APIView):
    """仪表盘统计接口。

    GET /api/dashboard/stats/
        返回各年级学生人数分布（一年级到高三）

    GET /api/dashboard/stats/?grade=GRADE_7
        返回指定年级下各班级的学生人数
    """
    permission_classes = [IsAuthenticated]

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
        grade = request.query_params.get('grade', '').strip()

        if grade:
            # 指定了年级 → 统计该年级下各班级的学生人数
            if grade not in GradeChoices.values:
                return fail(message=f'无效的年级参数: {grade}', code=1)

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
            distribution = []
            for value, label in GradeChoices.choices:
                count = StudentProfile.objects.filter(
                    class_id__grade=value
                ).count()
                distribution.append({'label': label, 'count': count})
            description = '各年级人数'

        data = DashboardStatsSerializer({
            'totals': totals,
            'distribution': distribution,
            'description': description,
        }).data

        return ok(data=data)
