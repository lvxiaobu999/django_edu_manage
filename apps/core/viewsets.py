from rest_framework import viewsets

from django_edu_manage.common.response import ok


class BaseViewSet(viewsets.ModelViewSet):
    """所有 ViewSet 的基类，统一 CRUD 响应的 message。

    覆盖 create / retrieve / update / partial_update / destroy / list
    六个标准动作，调用父类完成业务后，通过 ok() 包装为统一 JSON 结构：

        {"success": true, "code": 0, "message": "创建成功", "data": ..., "meta": ...}

    自定义 @action 不受影响，子类可继续直接调用 ok() / fail()。
    """

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return ok(data=response.data, message='创建成功')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return ok(data=response.data, message='查询成功')

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return ok(data=response.data, message='更新成功')

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return ok(data=response.data, message='更新成功')

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return ok(data=response.data, message='删除成功')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ok(data=response.data)
