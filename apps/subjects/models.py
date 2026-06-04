from django.db import models

# Create your models here.
# 科目模型
# 与 TeacherProfile 通过 M2M 关联（TeacherProfile.research_groups）。

from django.db import models


class Subjects(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='科目名称')

    class Meta:
        db_table = 'subjects'
        verbose_name = '科目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
