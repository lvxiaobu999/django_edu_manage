# 科目字典表。
# 科目是成绩记录（Score）的基础数据源之一，通过 FK 被引用。
# 使用 PROTECT 外键策略，确保有成绩引用的科目不会被误删。

from django.db import models


class Subjects(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='科目名称')

    class Meta:
        db_table = 'subjects'
        verbose_name = '科目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
