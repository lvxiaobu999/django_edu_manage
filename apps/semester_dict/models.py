# 学期字典表。
# 学期是考试计划（ExamPlan）的基础数据源，通过 FK 被引用。
# 每学年两个学期：第一学期（秋季）和第二学期（春季）。

from django.db import models


class Semester(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='学期标识', help_text='如：2025-2026-1')
    display_name = models.CharField(max_length=50, verbose_name='学期名称', help_text='如：2025-2026学年第一学期')

    class Meta:
        db_table = 'semester'
        verbose_name = '学期'
        verbose_name_plural = verbose_name
        ordering = ['-name']

    def __str__(self):
        return self.display_name
