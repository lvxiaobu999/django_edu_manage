from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.core.choices import (
    ExamTypeChoices,
    GenderChoices,
    GradeChoices,
    RoleChoices,
)
from django_edu_manage.common.response import ok

CHOICES_REGISTRY = {
    'roles': RoleChoices,
    'grades': GradeChoices,
    'exam_types': ExamTypeChoices,
    'genders': GenderChoices,
}


class ChoicesView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary='获取枚举值',
        description='返回角色、年级、考试类型、性别等枚举。可选参数 key 指定只返回某一类。',
        parameters=[
            OpenApiParameter(name='key', description='枚举键名', required=False, type=str,
                             enum=list(CHOICES_REGISTRY.keys())),
        ],
    )
    def get(self, request):
        key = request.query_params.get('key', '').strip()

        if key:
            if key not in CHOICES_REGISTRY:
                return ok(data={})
            choices_cls = CHOICES_REGISTRY[key]
            result = [
                {'value': value, 'label': label}
                for value, label in choices_cls.choices
            ]
            return ok(data={key: result})

        data = {}
        for name, choices_cls in CHOICES_REGISTRY.items():
            data[name] = [
                {'value': value, 'label': label}
                for value, label in choices_cls.choices
            ]
        return ok(data=data)
