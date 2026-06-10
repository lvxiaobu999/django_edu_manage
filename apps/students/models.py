from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.choices import GenderChoices


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='用户',
    )
    stu_no = models.CharField(max_length=20, unique=True, verbose_name='学号')
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
    class_id = models.ForeignKey(
        'dicts.ClassDict',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='所在班级',
    )

    class Meta:
        db_table = 'student_profile'        # 保持原表名，不丢数据
        verbose_name = '学生简介'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.realname}({self.stu_no})'
