# 成绩记录表 —— 核心枢纽。
# 这张表将学生（StudentProfile）、考试（ExamPlan）和科目（Subjects）绑定在一起。
# 通过 student → StudentProfile.class_id → Classes 链式关联，
# 系统天然就能知道每笔成绩属于哪个年级哪个班。

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Score(models.Model):
    # 通过 StudentProfile 可级联找到班级、年级信息
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='学生',
    )
    exam = models.ForeignKey(
        'exam.ExamPlan',
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='考试',
    )
    # PROTECT：科目被成绩引用后不可删除，防止数据悬空
    subject = models.ForeignKey(
        'dicts.SubjectDict',
        on_delete=models.PROTECT,
        related_name='scores',
        verbose_name='科目',
    )
    # DecimalField 支持半分布分（如 99.5），max_digits=5 支持 0.0 ~ 999.9
    score = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(999.9)],
        verbose_name='分数',
    )

    class Meta:
        db_table = 'score'
        verbose_name = '成绩记录'
        verbose_name_plural = verbose_name
        ordering = ['exam', 'student', 'subject']
        constraints = [
            # 同一学生 + 同一考试 + 同一科目只能有一条成绩
            models.UniqueConstraint(
                fields=['student', 'exam', 'subject'],
                name='unique_student_exam_subject',
            ),
        ]

    def __str__(self):
        return f'{self.student.realname} - {self.subject.name}: {self.score}'
