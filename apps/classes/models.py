from django.db import models


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


class Classes(models.Model):
    grade = models.CharField(
        max_length=20,
        choices=GradeChoices.choices,
        verbose_name='年级',
    )
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
        db_table = 'classes'
        verbose_name = '班级'
        verbose_name_plural = verbose_name
        ordering = ['grade', 'name']
        constraints = [
            models.UniqueConstraint(fields=['grade', 'name'], name='unique_grade_class'),
        ]

    def __str__(self):
        return f'{self.get_grade_display()}{self.name}'
