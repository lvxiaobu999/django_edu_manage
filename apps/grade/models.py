from django.db import models


class Grade(models.Model):
    """年级模型：一个年级可以包含多个班级。"""

    name = models.CharField(max_length=50, unique=True, verbose_name='年级名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='年级编码')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序值')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = '年级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

