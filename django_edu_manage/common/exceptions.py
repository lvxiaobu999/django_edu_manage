from datetime import datetime, timezone

from rest_framework.views import exception_handler


def _extract_message(detail):
    """从 DRF 的错误 detail 中提取第一条可读消息。"""
    if isinstance(detail, dict):
        for value in detail.values():
            if isinstance(value, list) and value:
                return str(value[0])
            if isinstance(value, str):
                return value
        return '请求参数有误'
    if isinstance(detail, list) and detail:
        return str(detail[0])
    return str(detail)


def unified_exception_handler(exc, context):
    """将 DRF 异常转为统一响应格式。"""
    response = exception_handler(exc, context)

    if response is None:
        return None

    request_id = ''
    request = context.get('request')
    if request:
        request_id = getattr(request, 'request_id', '')

    response.data = {
        'success': False,
        'code': response.status_code,
        'message': _extract_message(response.data),
        'data': response.data,
        'meta': {
            'requestId': request_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        },
    }
    return response
