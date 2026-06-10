from django.contrib import admin

from apps.teachers.models import TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'realname', 'gender', 'age', 'phone', 'email', 'address']
    search_fields = ['emp_no', 'realname', 'phone']
    list_filter = ['gender']
    filter_horizontal = ['research_groups', 'class_ids']
