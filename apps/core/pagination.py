from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """标准分页器，基于页码的翻页方式。

    用法：在 ViewSet 上加一行即可启用分页，
        class UserViewSet(ModelViewSet):
            pagination_class = StandardResultsSetPagination

    前端请求示例：
        GET /api/users/                        → 第 1 页，每页 10 条
        GET /api/users/?page=2                 → 第 2 页
        GET /api/users/?page=1&size=20         → 第 1 页，每页 20 条

    响应的 data 字段结构（由 UnifiedJSONRenderer 包裹后）：
        {
            "count": 150,         // 总记录数
            "next": "...?page=2", // 下一页 URL，最后一页为 null
            "previous": null,     // 上一页 URL，第一页为 null
            "results": [...]      // 当前页数据列表
        }
    """

    # 默认每页条数。不传 ?size 时生效
    page_size = 10

    # 前端传入页码的查询参数名
    page_query_param = 'page'

    # 前端传入每页条数的查询参数名。未设置时不允许前端控制页大小
    page_size_query_param = 'pageSize'

    # 前端能请求的最大单页数据量，防止 ?size=10000 拖垮数据库
    max_page_size = 100

    def get_paginated_response(self, data):
        """覆写父类方法，返回 DRF 标准的 {count, next, previous, results} 结构。

        这里不直接包裹成项目统一格式（ApiResponse），原因是：
        UnifiedJSONRenderer 会拦截所有 DRF 响应，自动将本方法返回的 dict
        作为 data 字段值，包裹为 {success, code, message, data, meta}。

        如果这里直接返回 ApiResponse，会造成二次包裹 —— 内层被 renderer
        当成普通 data 再次塞进外层，结构就乱了。
        """
        return Response({
            'total': self.page.paginator.count,
            'page': self.page.number,
            'pageSize': self.get_page_size(self.request),
            'totalPages': self.page.paginator.num_pages,
            'results': data,
        })
