from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """系统用户模型。"""

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', '管理员'
        TEACHER = 'TEACHER', '老师'
        STUDENT = 'STUDENT', '学生'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='角色',
    )
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='手机号')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username} - {self.get_role_display()}'


class StudentProfile(models.Model):
    """学生档案：一个班级可以有多个学生。"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='用户',
    )
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    class_group = models.ForeignKey(
        'classes.Class',
        on_delete=models.PROTECT,
        related_name='students',
        null=True,
        blank=True,
        verbose_name='所属班级',
    )
    guardian_phone = models.CharField(max_length=15, blank=True, verbose_name='家长联系方式')

    class Meta:
        verbose_name = '学生档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'学生档案: {self.user.real_name or self.user.username}'

    @property
    def grade(self):
        """通过班级反查学生所在年级，方便后续模板或后台直接使用。"""
        return self.class_group.grade if self.class_group_id else None


class TeacherProfile(models.Model):
    """教师档案。"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='用户',
    )
    department = models.CharField(max_length=50, verbose_name='教研组')
    hire_date = models.DateField(null=True, blank=True, verbose_name='入职时间')

    class Meta:
        verbose_name = '教师档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'教师档案: {self.user.real_name or self.user.username}'
