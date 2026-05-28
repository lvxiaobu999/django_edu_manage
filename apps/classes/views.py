from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.classes.models import Classes
from apps.classes.serializers import ClassesSerializer


# ModelViewSet 自动提供 list/create/retrieve/update/destroy 五个接口
class ClassesViewSet(viewsets.ModelViewSet):
    # select_related('headmaster__user')：SQL 关联查询优化
    # __user 是因为 TeacherProfile 有一个 user 字段，一次性 JOIN 取出关联数据
    # 避免 N+1 查询：每个班级单独查班主任信息会多出 N 条 SQL
    queryset = Classes.objects.select_related('headmaster__user')
    serializer_class = ClassesSerializer
    permission_classes = [IsAuthenticated]
