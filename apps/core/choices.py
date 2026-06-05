# apps/core/choices.py
from django.db import models

# 角色枚举
class RoleChoices(models.TextChoices):
    ADMIN = 'ADMIN', '管理员'
    TEACHER = 'TEACHER', '老师'
    STUDENT = 'STUDENT', '学生'

# 年级枚举
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

# 考试类型
class ExamTypeChoices(models.TextChoices):
    MONTHLY = 'MONTHLY', '月考'
    MOCK = 'MOCK', '模拟考'
    MIDTERM = 'MIDTERM', '期中'
    FINAL = 'FINAL', '期末'


# 性别
class GenderChoices(models.TextChoices):
    MALE = 'MALE', '男'
    FEMALE = 'FEMALE', '女'