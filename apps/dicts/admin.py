from django.contrib import admin

from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict


@admin.register(SubjectDict)
class SubjectDictAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(SemesterDict)
class SemesterDictAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name']
    search_fields = ['name', 'display_name']


@admin.register(ResearchGroupDict)
class ResearchGroupDictAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ClassDict)
class ClassDictAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'headmaster']
    list_filter = ['grade']
    search_fields = ['name']
    autocomplete_fields = ['headmaster']
