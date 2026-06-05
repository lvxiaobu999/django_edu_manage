# 考试模块 —— 考试计划（ExamPlan）是考试信息的独立实体。
# 不把考试信息直接挂在成绩表里，而是建立独立的"考试实体"。
# 考试名称由学期、年级、考试类型自动拼接生成，如"2025-2026学年第一学期高一期中考试"。

from django.db import models

from apps.core.choices import ExamTypeChoices, GradeChoices

class ExamPlan(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name='考试名称')
    exam_type = models.CharField(
        max_length=20,
        choices=ExamTypeChoices.choices,
        verbose_name='考试类型',
    )
    exam_date = models.DateField(verbose_name='考试日期')
    grade = models.CharField(
        max_length=20,
        choices=GradeChoices.choices,
        verbose_name='所属年级',
    )
    semester = models.ForeignKey(
        'dicts.SemesterDict',
        on_delete=models.PROTECT,
        related_name='exams',
        verbose_name='所属学期',
    )

    class Meta:
        db_table = 'exam_plan'
        verbose_name = '考试计划'
        verbose_name_plural = verbose_name
        ordering = ['-exam_date', 'grade']

    def __str__(self):
        return self.name or self.generate_name()

    def generate_name(self):
        semester_str = self.semester.display_name
        grade_str = self.get_grade_display()
        exam_str = self.get_exam_type_display()
        # 月考/模拟考本身已含"考"，不再追加"考试"后缀
        if exam_str.endswith('考'):
            return f'{semester_str}{grade_str}{exam_str}试'
        return f'{semester_str}{grade_str}{exam_str}考试'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.generate_name()
        super().save(*args, **kwargs)
