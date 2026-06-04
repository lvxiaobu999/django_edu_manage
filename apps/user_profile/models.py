from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# === 性别枚举 ===
class GenderChoices(models.TextChoices):
    MALE = 'MALE', '男'
    FEMALE = 'FEMALE', '女'


# === 老师简介 ===
# OneToOneField：每个 User（role=TEACHER）只有一份简介，删除 User 时自动级联删除
class TeacherProfile(models.Model):
    # settings.AUTH_USER_MODEL = 'users.User'，避免硬编码具体类，保持灵活性
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',  # 反向查：user.teacher_profile
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
    # M2M 字符串引用 'research_group.ResearchGroup'，跨 app 延迟加载，避免循环导入
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


# === 学生简介 ===
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
    # ForeignKey：一个学生属于一个班级，班级删除时学生保留（SET_NULL）
    class_id = models.ForeignKey(
        'dicts.ClassDict',
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
