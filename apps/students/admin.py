from django.contrib import admin

from apps.students.models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['stu_no', 'realname', 'gender', 'age', 'phone', 'email', 'address', 'class_id']
    search_fields = ['stu_no', 'realname', 'phone']
    list_filter = ['gender']
