# 教研组模型：从 user_profile 拆分出来的独立 app。
# 与 TeacherProfile 通过 M2M 关联（TeacherProfile.research_groups）。

from django.db import models


class ResearchGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='教研组名称')

    class Meta:
        db_table = 'research_group'
        verbose_name = '教研组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
