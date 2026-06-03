# dashboard 路由：
#   GET /api/dashboard/stats         → DashboardStatsView (全校统计)
#   GET /api/dashboard/stats?grade=GRADE_7 → DashboardStatsView (某年级下的班级)

from django.urls import path

from apps.dashboard.views import DashboardStatsView

urlpatterns = [
    path('stats', DashboardStatsView.as_view(), name='dashboard-stats'),
]
