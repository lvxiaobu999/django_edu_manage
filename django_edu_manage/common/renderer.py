from datetime import datetime, timezone

from rest_framework.renderers import JSONRenderer


class UnifiedJSONRenderer(JSONRenderer):
    """自动将 DRF 视图的返回值包裹为统一响应格式。

    只处理 JSON 格式的响应（Browsable API 等不走这个渲染器）。
    如果视图已经返回 ApiResponse 格式的数据则跳过包裹。
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        request_id = ''
        if renderer_context and 'request' in renderer_context:
            request_id = getattr(renderer_context['request'], 'request_id', '')

        # 已经是统一格式，补全 requestId 后直接渲染
        if isinstance(data, dict) and {'success', 'code', 'meta'}.issubset(data):
            if request_id:
                data['meta'].setdefault('requestId', request_id)
            return super().render(data, accepted_media_type, renderer_context)

        # 空响应（如 204 No Content）不处理
        if data is None:
            return super().render(data, accepted_media_type, renderer_context)

        unified = {
            'success': True,
            'code': 0,
            'message': 'ok',
            'data': data,
            'meta': {
                'requestId': request_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
            },
        }
        return super().render(unified, accepted_media_type, renderer_context)
