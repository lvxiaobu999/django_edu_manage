from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleChoices(models.TextChoices):
    ADMIN = 'ADMIN', '管理员'
    TEACHER = 'TEACHER', '老师'
    STUDENT = 'STUDENT', '学生'


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
        verbose_name='角色',
    )
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')
    is_approved = models.BooleanField(default=False, verbose_name='是否审核通过')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username}({self.get_role_display()})'
