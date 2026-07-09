"""成绩 ViewSet —— 完整 CRUD，支持按考试、科目、学生、年级、班级筛选。"""

from zipfile import BadZipFile

from django.http import HttpResponse
from openpyxl.utils.exceptions import InvalidFileException
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.core.choices import GradeChoices
from apps.core.pagination import StandardResultsSetPagination
from apps.core.query_params import get_choice_param, get_int_param, get_str_param
from apps.core.viewsets import BaseViewSet
from apps.score.importers import build_score_import_template, import_scores_from_excel
from apps.score.models import Score
from apps.score.serializers import (
    ScoreImportExcelSerializer,
    ScoreImportResultSerializer,
    ScoreSerializer,
)
from django_edu_manage.common.response import fail, ok


@extend_schema_view(
    list=extend_schema(
        summary='成绩列表',
        description='所有成绩记录，预加载学生/考试/科目关联信息。'
                    '支持按考试、科目、学生姓名、年级、班级筛选。',
        parameters=[
            OpenApiParameter(name='exam', description='考试 ID 精确匹配', required=False, type=int),
            OpenApiParameter(name='subject', description='科目 ID 精确匹配', required=False, type=int),
            OpenApiParameter(name='student', description='学生姓名模糊搜索', required=False, type=str),
            OpenApiParameter(name='grade', description='年级编码精确匹配', required=False, type=str,
                             enum=GradeChoices.values),
            OpenApiParameter(name='class_id', description='班级 ID 精确匹配', required=False, type=int),
        ],
    ),
    create=extend_schema(summary='录入成绩', description='新增一条成绩记录（同一学生+考试+科目不可重复）。'),
    retrieve=extend_schema(summary='查看成绩详情'),
    update=extend_schema(summary='全量更新成绩'),
    partial_update=extend_schema(summary='部分更新成绩'),
    destroy=extend_schema(summary='删除成绩'),
)
class ScoreViewSet(BaseViewSet):
    # 成绩列表会展示学生、考试、科目名称，并支持按学生班级/年级筛选。
    # select_related 一次性预加载这些外键链路，避免每条成绩记录分别查询关联表。
    queryset = Score.objects.select_related(
        'student',
        'student__class_id',
        'exam',
        'subject',
    ).all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # 和 queryset 保持一致：先准备好序列化和筛选会用到的关联对象。
        qs = Score.objects.select_related(
            'student',
            'student__class_id',
            'exam',
            'subject',
        )

        # exam/subject 是外键 ID，先转整数再过滤，非法输入会返回统一参数错误。
        exam = get_int_param(self.request.query_params, 'exam')
        if exam:
            qs = qs.filter(exam_id=exam)

        subject = get_int_param(self.request.query_params, 'subject')
        if subject:
            qs = qs.filter(subject_id=subject)

        # student 按学生真实姓名模糊搜索，保留字符串查询能力。
        student = get_str_param(self.request.query_params, 'student')
        if student:
            qs = qs.filter(student__realname__icontains=student)

        # grade/class_id 通过 student -> class_id 这条关系过滤，补齐接口文档中声明的筛选能力。
        grade = get_choice_param(self.request.query_params, 'grade', GradeChoices.values)
        if grade:
            qs = qs.filter(student__class_id__grade=grade)

        class_id = get_int_param(self.request.query_params, 'class_id')
        if class_id:
            qs = qs.filter(student__class_id_id=class_id)

        # 按考试、学生、科目排序，成绩列表更便于前端分组展示，也避免分页顺序不稳定。
        return qs.order_by('exam_id', 'student_id', 'subject_id')

    @extend_schema(
        summary='下载成绩 Excel 导入模板',
        description='下载学生成绩导入模板。模板包含填写 sheet、考试列表 sheet、科目列表 sheet，方便录入考试ID和科目ID。',
        responses={
            (200, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'): OpenApiTypes.BINARY,
        },
    )
    @action(detail=False, methods=['get'], url_path='import-template')
    def import_template(self, request):
        content = build_score_import_template()
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="score_import_template.xlsx"'
        return response

    @extend_schema(
        summary='Excel 导入学生成绩',
        description=(
            '上传 .xlsx 文件批量导入学生成绩。'
            '必填列为“学号、分数”，并且“考试ID/考试名称”二选一、“科目ID/科目名称”二选一。'
            '默认遇到已存在成绩时报错；传 overwrite=true 时会覆盖更新已有成绩。'
            '导入前会先校验整张表，任意行有错误则本次不写入任何数据。'
        ),
        request=ScoreImportExcelSerializer,
        responses={200: ScoreImportResultSerializer},
    )
    @action(
        detail=False,
        methods=['post'],
        url_path='import-excel',
        parser_classes=[MultiPartParser, FormParser],
    )
    def import_excel(self, request):
        serializer = ScoreImportExcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = import_scores_from_excel(
                serializer.validated_data['file'],
                overwrite=serializer.validated_data.get('overwrite', False),
            )
        except (BadZipFile, InvalidFileException):
            return fail(
                message='Excel 文件格式无效，请上传 .xlsx 文件',
                code=400,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if result['errors']:
            return fail(
                message='导入失败，请根据 errors 修正 Excel 后重新上传',
                code=400,
                data=result,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return ok(data=result, message='导入成功')
