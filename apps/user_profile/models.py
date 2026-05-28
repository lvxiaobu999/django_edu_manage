from django.conf import settings
from django.db import models


# === 教研组 ===
class ResearchGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='教研组名称')

    class Meta:
        db_table = 'research_group'
        verbose_name = '教研组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# === 老师简介 ===
# OneToOneField：每个 User（role=TEACHER）只有一份老师简介，反之亦然
class TeacherProfile(models.Model):
    # settings.AUTH_USER_MODEL 返回 'users.User'，避免硬编码具体 User 类
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        # CASCADE：删除 User 时，关联的 TeacherProfile 也会被删除
        on_delete=models.CASCADE,
        # related_name：从 User 反向获取 profile：
        #   user.teacher_profile → 返回 TeacherProfile 对象（因为 OneToOneField，返回单个）
        # 如果没设置，默认是 teacherprofile（模型名小写）
        related_name='teacher_profile',
        verbose_name='用户',
    )
    emp_no = models.CharField(max_length=20, unique=True, verbose_name='工号')
    realname = models.CharField(max_length=50, verbose_name='真实姓名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    address = models.CharField(max_length=200, blank=True, verbose_name='家庭住址')

    # ManyToManyField：多对多关系，一个老师可以属于多个教研组，一个教研组可以有多个老师
    # Django 会自动创建一张中间表来存储关联关系，不需要手动建
    research_groups = models.ManyToManyField(
        ResearchGroup,
        blank=True,
        related_name='teachers',
        verbose_name='所属教研组',
    )

    # 字符串形式引用跨模块模型 'classes.Classes'，避免循环导入
    # related_name='teachers'：从 Classes 反向查：classes_obj.teachers.all()
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

    # ForeignKey：一个学生只在一个班级，一个班级可以有多个学生
    # SET_NULL：班级被删除时，学生的 class_id 变为 NULL，保留学生数据
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
