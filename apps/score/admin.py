from django.contrib import admin

from apps.score.models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'score']
    list_filter = ['exam', 'subject']
    search_fields = ['student__realname', 'student__stu_no']
