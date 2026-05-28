from django.db import models


# === 年级枚举 ===
# 覆盖中小学常见年级（一年级到高三），使用 TextChoices 可在查询和展示之间切换
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

    # ForeignKey：一对多关系，一个班主任可以管多个班（实际通常一对一，但模型支持多班级）
    #
    # 为什么用字符串 'user_profile.TeacherProfile' 而不是直接 import？
    #   因为 classes 和 user_profile 互有引用（循环依赖），Django 的延迟加载
    #   允许用 "app_label.ModelName" 字符串形式引用，Django 启动时内部自动解析。
    #
    # on_delete=models.SET_NULL：班主任被删除时，班级的 headmaster 字段设为 NULL，
    #   而不是把班级也删了。保护数据完整性。
    #
    # related_name='headmaster_classes'：反向查询名。
    #   从 TeacherProfile 对象可以通过 teacher.headmaster_classes.all()
    #   获取该老师担任班主任的班级列表。
    #   如果不设置，Django 会自动生成（格式：类名小写_set），但容易和
    #   TeacherProfile.class_ids 的 related_name='teachers' 冲突，所以显式命名。
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
        # ordering：默认排序，查询会自动按年级→班级名排序
        ordering = ['grade', 'name']
        # UniqueConstraint：数据库唯一约束，同一个年级下不能有两个同名班级
        constraints = [
            models.UniqueConstraint(fields=['grade', 'name'], name='unique_grade_class'),
        ]

    def __str__(self):
        # get_grade_display() 返回年级中文，如 '七年级'
        return f'{self.get_grade_display()}{self.name}'
