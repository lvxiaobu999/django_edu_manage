
# Register your models here.
from django.contrib import admin

from apps.subjects.models import Subjects


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']