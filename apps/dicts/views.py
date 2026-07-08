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

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.choices import GradeChoices
from apps.core.pagination import StandardResultsSetPagination
from apps.core.query_params import get_choice_param, get_str_param
from apps.core.viewsets import BaseViewSet
from apps.dicts.models import ClassDict, ResearchGroupDict, SemesterDict, SubjectDict
from apps.dicts.serializers import (
    ClassDictSerializer,
    ClassSimpleSerializer,
    GradeClassesItemSerializer,
    ResearchGroupDictSerializer,
    SemesterDictSerializer,
    SubjectDictSerializer,
)
from django_edu_manage.common.response import ok


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
    # 字典表默认按 id 排序，保证分页/列表返回顺序稳定。
    queryset = SubjectDict.objects.order_by('id')
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
    # 学期通常希望最新的排在前面，因此按 name 倒序。
    queryset = SemesterDict.objects.order_by('-name')
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
    # 简单字典表使用稳定排序即可。
    queryset = ResearchGroupDict.objects.order_by('id')
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
    # headmaster 是外键，预加载后序列化 headmaster_name 不会再额外查库。
    # 按年级、班级名排序，方便前端直接展示年级下的班级列表。
    queryset = ClassDict.objects.select_related('headmaster').order_by('grade', 'name')
    serializer_class = ClassDictSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # select_related('headmaster')：预加载班主任的 TeacherProfile，
        # 后续 serializer 访问 headmaster.realname 时不会额外查库（避免 N+1）。
        # 参数填的是模型上的 FK 字段名 headmaster，不是数据库列名 headmaster_id。
        qs = ClassDict.objects.select_related('headmaster')

        # grade 是枚举字段，先校验再过滤，避免无效年级编码进入查询。
        grade = get_choice_param(self.request.query_params, 'grade', GradeChoices.values)
        if grade:
            # grade 是 ClassDict 自己的字段，直接用等值匹配
            qs = qs.filter(grade=grade)

        name = get_str_param(self.request.query_params, 'name')
        if name:
            # name__icontains：对 ClassDict.name 做忽略大小写的模糊匹配
            # 等价 SQL: WHERE dict_class.name LIKE '%name%' COLLATE NOCASE
            qs = qs.filter(name__icontains=name)

        headmaster = get_str_param(self.request.query_params, 'headmaster')
        if headmaster:
            # headmaster__realname__icontains：
            #   headmaster   → 沿 FK 跨到 teacher_profile 表
            #   realname     → teacher_profile 上的字段
            #   icontains    → 忽略大小写的 LIKE '%…%'
            # 等价 SQL: JOIN teacher_profile ON dict_class.headmaster_id = teacher_profile.id
            #           WHERE teacher_profile.realname LIKE '%headmaster%'
            qs = qs.filter(headmaster__realname__icontains=headmaster)

        # 筛选后仍保持统一排序，保证分页和下拉选项顺序稳定。
        return qs.order_by('grade', 'name')

    @extend_schema(
        summary='年级班级联动',
        description='返回所有年级及其下班级的级联数据，用于前端年级-班级二级联动下拉。',
        responses={200: GradeClassesItemSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='grade-classes')
    def grade_classes(self, request):
        """年级-班级二级联动接口。

        遍历所有年级枚举，按年级分组返回该年级下的班级列表。
        无班级的年级也返回，classes 为空数组。
        """
        # 一次查询所有班级，按年级+班级名排序；这里不再 print 调试信息，避免污染服务日志。
        all_classes = ClassDict.objects.order_by('grade', 'name')
        # 按年级分组
        grade_map = {}
        for c in all_classes:
            grade_map.setdefault(c.grade, []).append(c)

        result = []
        for g in GradeChoices:
            classes = grade_map.get(g.value, [])
            result.append({
                'grade_id': g.value,
                'grade_name': g.label,
                'classes': [
                    {'class_id': cls.id, 'class_name': cls.name}
                    for cls in classes
                ],
            })

        return ok(data=result, message='查询成功')
