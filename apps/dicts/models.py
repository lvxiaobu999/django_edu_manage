# 字典管理 —— 集中管理项目中所有字典表。
# 包含：科目字典、学期字典、教研组字典、班级字典、年级枚举。
# 统一放在一个 App 中，避免字典过度分散。

from django.db import models


# =========================== 年级枚举 ===========================
class GradeChoices(models.TextChoices):
    GRADE_1 = 'GRADE_1', '一年级'
    GRADE_2 = 'GRADE_2', '二年级'
    GRADE_3 = 'GRADE_3', '三年级'
    GRADE_4 = 'GRADE_4', '四年级'
    GRADE_5 = 'GRADE_5', '五年级'
    GRADE_6 = 'GRADE_6', '六年级'
    GRADE_7 = 'GRADE_7', '七年级'
    GRADE_8 = 'GRADE_8', '八年级'
    GRADE_9 = 'GRADE_9', '九年级'
    SENIOR_1 = 'SENIOR_1', '高一'
    SENIOR_2 = 'SENIOR_2', '高二'
    SENIOR_3 = 'SENIOR_3', '高三'


# =========================== 科目字典 ===========================
class SubjectDict(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='科目名称')

    class Meta:
        db_table = 'dict_subject'
        verbose_name = '科目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# =========================== 学期字典 ===========================
class SemesterDict(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='学期标识', help_text='如：2025-2026-1')
    display_name = models.CharField(max_length=50, verbose_name='学期名称', help_text='如：2025-2026学年第一学期')

    class Meta:
        db_table = 'dict_semester'
        verbose_name = '学期'
        verbose_name_plural = verbose_name
        ordering = ['-name']

    def __str__(self):
        return self.display_name


# =========================== 教研组字典 ===========================
class ResearchGroupDict(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='教研组名称')

    class Meta:
        db_table = 'dict_research_group'
        verbose_name = '教研组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# =========================== 班级字典 ===========================
class ClassDict(models.Model):
    grade = models.CharField(max_length=20, choices=GradeChoices.choices, verbose_name='年级')
    name = models.CharField(max_length=50, verbose_name='班级名称')
    headmaster = models.ForeignKey(
        'user_profile.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headmaster_classes',
        verbose_name='班主任',
    )

    class Meta:
        db_table = 'dict_class'
        verbose_name = '班级'
        verbose_name_plural = verbose_name
        ordering = ['grade', 'name']
        constraints = [
            models.UniqueConstraint(fields=['grade', 'name'], name='unique_grade_class'),
        ]

    def __str__(self):
        return f'{self.get_grade_display()}{self.name}'
