from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


# @admin.register(User)：Python 装饰器，等价于 admin.site.register(User, UserAdmin)
# 它把 User 模型注册到 Django Admin 后台，管理界面中就能看到用户管理
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # list_display：列表页展示哪些列
    list_display = ['username', 'email', 'phone', 'role', 'real_name', 'is_approved', 'is_active']
    # list_filter：右侧过滤栏
    list_filter = ['role', 'is_approved', 'is_active']
    # search_fields：搜索框可搜索的字段
    search_fields = ['username', 'email', 'phone', 'real_name']

    # fieldsets：编辑/新增页面的字段分组
    # BaseUserAdmin.fieldsets 是 Django 内置的（用户名、密码、权限等）
    # 这里追加一个"额外信息"分组，放入自定义字段
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('phone', 'role', 'real_name', 'is_approved')}),
    )
