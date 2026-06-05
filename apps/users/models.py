from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.choices import RoleChoices


# === 角色枚举 ===
# 继承 models.TextChoices 定义数据库枚举字段。
# 每个成员格式：数据库值 = '存储值', '人类可读名称'
# 比如数据库中存 'ADMIN'，通过 get_role_display() 显示为 '管理员'



# === 用户模型 ===
# 继承 AbstractUser（而非默认的 User），这是 Django 官方推荐的扩展方式。
# AbstractUser 已经自带 username、password、email、is_active 等字段，
# 我们只需要追加项目特有的字段即可。
#
# 重要：必须同步配置 settings.AUTH_USER_MODEL = 'users.User'，
# 告诉 Django "请用这个模型作为用户模型"。
class User(AbstractUser):
    # CharField：字符串字段，max_length 限制长度，blank=True 表示可选
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')

    # choices：限定字段只能从枚举中取值
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
        verbose_name='角色',
    )
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')

    # 审核状态：注册后为 False，管理员审核通过后改为 True
    is_approved = models.BooleanField(default=False, verbose_name='是否审核通过')

    class Meta:
        # db_table：自定义数据库表名（默认是 app_label_modelname）
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        # get_role_display() 返回的是角色枚举的中文名（如 '学生'）
        return f'{self.username}({self.get_role_display()})'
