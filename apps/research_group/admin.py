from django.contrib import admin

from apps.research_group.models import ResearchGroup


@admin.register(ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
