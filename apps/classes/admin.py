from django.contrib import admin

from apps.classes.models import Classes


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'headmaster']
    list_filter = ['grade']
    search_fields = ['name']
    # autocomplete_fields：外键选择框支持搜索自动补全，避免下拉框数据太多
    # 前提：关联的 TeacherProfile 的 Admin 也得有 search_fields
    autocomplete_fields = ['headmaster']
