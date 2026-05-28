from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone', 'role', 'real_name', 'is_approved', 'is_active']
    list_filter = ['role', 'is_approved', 'is_active']
    search_fields = ['username', 'email', 'phone', 'real_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('phone', 'role', 'real_name', 'is_approved')}),
    )
