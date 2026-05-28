from django.contrib import admin

from apps.user_profile.models import ResearchGroup, StudentProfile, TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'realname', 'phone', 'email']
    search_fields = ['emp_no', 'realname', 'phone']
    filter_horizontal = ['research_groups', 'class_ids']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['stu_no', 'realname', 'phone', 'email', 'class_id']
    search_fields = ['stu_no', 'realname', 'phone']


@admin.register(ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
