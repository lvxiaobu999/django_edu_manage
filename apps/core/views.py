from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.core.choices import (
    ExamTypeChoices,
    GenderChoices,
    GradeChoices,
    RoleChoices,
)
from django_edu_manage.common.response import ok

# 注册表：新增枚举在这里加一行即可，接口自动生效
CHOICES_REGISTRY = {
    'roles': RoleChoices,
    'grades': GradeChoices,
    'exam_types': ExamTypeChoices,
    'genders': GenderChoices,
}


class ChoicesView(APIView):
    """枚举值接口。

    GET /api/choices
        返回前端需要的所有枚举，格式：
        {
          "roles": [{"value": "ADMIN", "label": "管理员"}, ...],
          "grades": [{"value": "GRADE_1", "label": "一年级"}, ...],
          "exam_types": [{"value": "MONTHLY", "label": "月考"}, ...],
          "genders": [{"value": "MALE", "label": "男"}, ...]
        }

    GET /api/choices?key=roles
        只返回指定枚举
    """
    permission_classes = [AllowAny]

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
