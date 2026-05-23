from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StudentProfile, TeacherProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """扩展 Django 原生用户后台，展示项目自定义字段。"""

    fieldsets = UserAdmin.fieldsets + (
        ('角色与附加信息', {'fields': ('role', 'real_name', 'phone_number')}),
    )
    list_display = ('username', 'email', 'real_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'real_name', 'phone_number')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'class_group', 'guardian_phone')
    list_filter = ('class_group__grade', 'class_group')
    search_fields = ('student_id', 'user__username', 'user__real_name')
    autocomplete_fields = ('user', 'class_group')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'hire_date')
    search_fields = ('user__username', 'user__real_name', 'department')
    autocomplete_fields = ('user',)
