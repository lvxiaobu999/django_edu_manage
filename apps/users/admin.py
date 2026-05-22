from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TeacherProfile

# 扩展原生的 UserAdmin 以显示我们新增的字段
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('角色与附加信息', {'fields': ('role', 'real_name', 'phone_number')}),
    )
    list_display = ('username', 'email', 'real_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)