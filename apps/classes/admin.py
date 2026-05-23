from django.contrib import admin

from .models import Class


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'code', 'homeroom_teacher', 'capacity', 'is_active')
    list_filter = ('grade', 'is_active')
    search_fields = ('name', 'code', 'grade__name')
    autocomplete_fields = ('grade', 'homeroom_teacher')

