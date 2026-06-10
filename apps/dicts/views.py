"""
字典 ViewSet —— 为 Subject / Semester / ResearchGroup / Class 四张字典表
提供 list / create / retrieve / update / destroy 五个标准 REST 接口，
配合 NoSlashRouter 自动生成无斜杠后缀的 URL。

关于 select_related 的取值：
    参数填的是模型上 ForeignKey / OneToOneField 字段的 Python 属性名，
    即你在模型里写的那个名字，不是数据库列名（Django 会自动加 _id 后缀）。
    例如 ClassDict.headmaster 是 FK → TeacherProfile，写 'headmaster' 即可。
    跨多层关联用双下划线：'headmaster__user' 会一次性 JOIN 两张表。

关于字段查找（field lookup），以 ClassDictViewSet 为例：
    name__icontains
        → 对 ClassDict.name 做 LIKE '%keyword%' 模糊匹配，忽略大小写。
    headmaster__realname__icontains
        → 先跨 FK 到 TeacherProfile，再对其 realname 做 case-insensitive 模糊匹配。
        等价 SQL：JOIN teacher_profile ON …
                 WHERE teacher_profile.realname LIKE '%keyword%'
    通用规则：字段名__查询方式，多层关联用 __ 串联。
"""

from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.pagination import StandardResultsSetPagination
from apps.core.viewsets import BaseViewSet
from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict
from apps.dicts.serializers import (
    ClassDictSerializer,
    ResearchGroupDictSerializer,
    SemesterDictSerializer,
    SubjectDictSerializer,
)


@extend_schema_view(
    list=extend_schema(summary='科目列表', description='返回所有科目的 id 和 name。'),
    create=extend_schema(summary='新增科目'),
    retrieve=extend_schema(summary='查看科目详情'),
    update=extend_schema(summary='全量更新科目'),
    partial_update=extend_schema(summary='部分更新科目'),
    destroy=extend_schema(summary='删除科目'),
)
class SubjectDictViewSet(BaseViewSet):
    """科目字典。"""
    queryset = SubjectDict.objects.all()
    serializer_class = SubjectDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(summary='学期列表'),
    create=extend_schema(summary='新增学期'),
    retrieve=extend_schema(summary='查看学期详情'),
    update=extend_schema(summary='全量更新学期'),
    partial_update=extend_schema(summary='部分更新学期'),
    destroy=extend_schema(summary='删除学期'),
)
class SemesterDictViewSet(BaseViewSet):
    """学期字典。"""
    queryset = SemesterDict.objects.all()
    serializer_class = SemesterDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(summary='教研组列表'),
    create=extend_schema(summary='新增教研组'),
    retrieve=extend_schema(summary='查看教研组详情'),
    update=extend_schema(summary='全量更新教研组'),
    partial_update=extend_schema(summary='部分更新教研组'),
    destroy=extend_schema(summary='删除教研组'),
)
class ResearchGroupDictViewSet(BaseViewSet):
    """教研组字典 — 字段简单，无关联表。"""
    queryset = ResearchGroupDict.objects.all()
    serializer_class = ResearchGroupDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary='班级列表',
        description='支持按年级、班级名、班主任姓名筛选。',
        parameters=[
            OpenApiParameter(name='grade', description='年级编码', required=False, type=str,
                             enum=['GRADE_1','GRADE_2','GRADE_3','GRADE_4','GRADE_5','GRADE_6',
                                   'GRADE_7','GRADE_8','GRADE_9','SENIOR_1','SENIOR_2','SENIOR_3']),
            OpenApiParameter(name='name', description='班级名模糊搜索', required=False, type=str),
            OpenApiParameter(name='headmaster', description='班主任姓名模糊搜索', required=False, type=str),
        ],
    ),
    create=extend_schema(summary='新增班级'),
    retrieve=extend_schema(summary='查看班级详情'),
    update=extend_schema(summary='全量更新班级'),
    partial_update=extend_schema(summary='部分更新班级'),
    destroy=extend_schema(summary='删除班级'),
)
class ClassDictViewSet(BaseViewSet):
    """班级字典 — 支持按年级、班级名、班主任姓名筛选。

    查询参数：
        grade      — 年级编码精确匹配，如 ?grade=GRADE_1
        name       — 班级名模糊搜索（忽略大小写），如 ?name=1  → 匹配 "1班"、"10班"、"11班"
        headmaster — 班主任姓名模糊搜索（忽略大小写），如 ?headmaster=张
    """
    queryset = ClassDict.objects.all()
    serializer_class = ClassDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # select_related('headmaster')：预加载班主任的 TeacherProfile，
        # 后续 serializer 访问 headmaster.realname 时不会额外查库（避免 N+1）。
        # 参数填的是模型上的 FK 字段名 headmaster，不是数据库列名 headmaster_id。
        qs = ClassDict.objects.select_related('headmaster')

        grade = self.request.query_params.get('grade', '').strip()
        if grade:
            # grade 是 ClassDict 自己的字段，直接用等值匹配
            qs = qs.filter(grade=grade)

        name = self.request.query_params.get('name', '').strip()
        if name:
            # name__icontains：对 ClassDict.name 做忽略大小写的模糊匹配
            # 等价 SQL: WHERE dict_class.name LIKE '%name%' COLLATE NOCASE
            qs = qs.filter(name__icontains=name)

        headmaster = self.request.query_params.get('headmaster', '').strip()
        if headmaster:
            # headmaster__realname__icontains：
            #   headmaster   → 沿 FK 跨到 teacher_profile 表
            #   realname     → teacher_profile 上的字段
            #   icontains    → 忽略大小写的 LIKE '%…%'
            # 等价 SQL: JOIN teacher_profile ON dict_class.headmaster_id = teacher_profile.id
            #           WHERE teacher_profile.realname LIKE '%headmaster%'
            qs = qs.filter(headmaster__realname__icontains=headmaster)

        return qs
