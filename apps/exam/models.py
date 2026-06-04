# 考试模块 —— 考试计划（ExamPlan）是考试信息的独立实体。
# 不把考试信息直接挂在成绩表里，而是建立独立的"考试实体"。
# 这样即使名字都叫"第一次模拟考"，只要所属学期/日期不同，就是两条互不干扰的记录。

from django.db import models

from apps.classes.models import GradeChoices


class ExamTypeChoices(models.TextChoices):
    MONTHLY = 'MONTHLY', '月考'
    MOCK = 'MOCK', '模拟考'
    MIDTERM = 'MIDTERM', '期中'
    FINAL = 'FINAL', '期末'


class ExamPlan(models.Model):
    name = models.CharField(max_length=200, verbose_name='考试名称')
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
    # FK → Semester（学期字典），PROTECT 策略防止有考试记录时误删学期
    semester = models.ForeignKey(
        'semester_dict.Semester',
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
        return f'{self.name}（{self.get_exam_type_display()}）'
