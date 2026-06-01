import uuid


class RequestIdMiddleware:
    """为每个请求生成唯一的 request_id，挂载到 request.request_id。

    之后 unified_exception_handler 和 UnifiedJSONRenderer 会读取它，
    写入响应的 meta.requestId 字段，方便前后端日志追踪。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        return self.get_response(request)
