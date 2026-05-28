from django.contrib import admin

from apps.classes.models import Classes


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'headmaster']
    list_filter = ['grade']
    search_fields = ['name']
    autocomplete_fields = ['headmaster']
