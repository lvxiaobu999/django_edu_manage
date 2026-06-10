from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.choices import GenderChoices


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='用户',
    )
    emp_no = models.CharField(max_length=20, unique=True, verbose_name='工号')
    realname = models.CharField(max_length=50, verbose_name='真实姓名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    address = models.CharField(max_length=200, blank=True, verbose_name='家庭住址')
    age = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(150)],
        verbose_name='年龄',
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
        verbose_name='性别',
    )
    research_groups = models.ManyToManyField(
        'dicts.ResearchGroupDict',
        blank=True,
        related_name='teachers',
        verbose_name='所属教研组',
    )
    class_ids = models.ManyToManyField(
        'dicts.ClassDict',
        blank=True,
        related_name='teachers',
        verbose_name='所教班级',
    )

    class Meta:
        db_table = 'teacher_profile'
        verbose_name = '老师简介'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.realname}({self.emp_no})'
