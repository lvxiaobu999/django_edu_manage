from django.contrib import admin

from apps.user_profile.models import StudentProfile, TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'realname', 'gender', 'age', 'phone', 'email']
    search_fields = ['emp_no', 'realname', 'phone']
    list_filter = ['gender']
    # filter_horizontal：M2M 字段的双栏选择控件，比默认多选下拉框好用
    filter_horizontal = ['research_groups', 'class_ids']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['stu_no', 'realname', 'gender', 'age', 'phone', 'email', 'class_id']
    search_fields = ['stu_no', 'realname', 'phone']
    list_filter = ['gender']
