from django.contrib import admin

from apps.exam.models import ExamPlan


@admin.register(ExamPlan)
class ExamPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'exam_date', 'grade', 'semester']
    list_filter = ['exam_type', 'grade', 'semester']
    search_fields = ['name']
