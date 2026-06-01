import uuid

from django_edu_manage.common.logging import set_request_id


class RequestIdMiddleware:
    """为每个请求生成唯一的 request_id。

    同时挂载到两处：
    - request.request_id：供 UnifiedJSONRenderer / exception_handler 写入响应体
    - thread-local：供 RequestIdFilter 注入每一条日志记录
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        set_request_id(request_id)
        return self.get_response(request)
