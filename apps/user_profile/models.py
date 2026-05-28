from django.conf import settings
from django.db import models


class ResearchGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='教研组名称')

    class Meta:
        db_table = 'research_group'
        verbose_name = '教研组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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
    research_groups = models.ManyToManyField(
        ResearchGroup,
        blank=True,
        related_name='teachers',
        verbose_name='所属教研组',
    )
    class_ids = models.ManyToManyField(
        'classes.Classes',
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
    class_id = models.ForeignKey(
        'classes.Classes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='所在班级',
    )

    class Meta:
        db_table = 'student_profile'
        verbose_name = '学生简介'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.realname}({self.stu_no})'
