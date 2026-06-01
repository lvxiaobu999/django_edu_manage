import uuid
from datetime import datetime, timezone

from rest_framework import status
from rest_framework.response import Response


class ApiResponse(Response):
    """统一响应格式。

    所有成功和失败的 API 响应都通过这个类构建，保证前端拿到的 JSON 结构一致：

        {
            "success": true,
            "code": 0,
            "message": "ok",
            "data": {...},
            "meta": {
                "requestId": "uuid",
                "timestamp": "2025-01-01T00:00:00+00:00"
            }
        }
    """

    def __init__(self, data=None, code=0, message='ok', success=True,
                 status_code=None, request_id='', **kwargs):
        body = {
            'success': success,
            'code': code,
            'message': message,
            'data': data if data is not None else None,
            'meta': {
                'requestId': request_id or str(uuid.uuid4()),
                'timestamp': datetime.now(timezone.utc).isoformat(),
            },
        }
        if status_code is None:
            status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        super().__init__(data=body, status=status_code, **kwargs)


def ok(data=None, message='ok', status_code=None):
    """快捷成功响应。"""
    return ApiResponse(data=data, code=0, message=message, success=True,
                       status_code=status_code)


def fail(message='error', code=1, data=None, status_code=None):
    """快捷失败响应。"""
    return ApiResponse(data=data, code=code, message=message, success=False,
                       status_code=status_code)
