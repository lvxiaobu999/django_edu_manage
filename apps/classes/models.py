from django.conf import settings
from django.db import models


class Class(models.Model):
    """班级模型：一个班级属于一个年级，一个班级可以包含多个学生。"""

    grade = models.ForeignKey(
        'grade.Grade',
        on_delete=models.PROTECT,
        related_name='classes',
        verbose_name='所属年级',
    )
    name = models.CharField(max_length=50, verbose_name='班级名称')
    code = models.CharField(max_length=20, blank=True, verbose_name='班级编码')
    homeroom_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'TEACHER'},
        related_name='managed_classes',
        verbose_name='班主任',
    )
    capacity = models.PositiveIntegerField(default=0, verbose_name='班级容量')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['grade__sort_order', 'grade_id', 'name']
        constraints = [
            models.UniqueConstraint(fields=['grade', 'name'], name='unique_class_name_per_grade'),
        ]
        verbose_name = '班级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.grade.name} {self.name}'

