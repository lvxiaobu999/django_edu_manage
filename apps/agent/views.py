"""AI Agent 视图层 —— 负责接收 HTTP 请求、参数校验、调用 Service，统一响应。

接口：
    POST /api/agent/chat/           — 单次问答
    POST /api/agent/chat/session/   — 带记忆的多轮对话
    DELETE /api/agent/chat/session/ — 清除会话记忆
"""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.agent.serializers import ChatSerializer, ChatWithMemorySerializer
from apps.agent.services.engine import chat, chat_with_memory, clear_session
from django_edu_manage.common.response import fail, ok


@extend_schema_view(
    post=extend_schema(
        summary='AI 单次问答',
        description=(
            '向 AI 助手提问，获取单次回答（不保留对话历史）。\n\n'
            '支持的提问类型：\n'
            '- 学校成立年份、创办时间\n'
            '- 校训、办学理念\n'
            '- 校区分布与规模\n'
            '- 历史沿革\n'
            '- 校长、党委书记等基础信息'
        ),
        request=ChatSerializer,
    ),
)
class ChatView(APIView):
    """单次问答 —— 每次请求独立，不保留历史。"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return fail(message='参数校验失败', data=serializer.errors)

        query = serializer.validated_data['query']

        try:
            answer = chat(query)
            return ok(data={'answer': answer}, message='查询成功')
        except ValueError as e:
            # LLM 配置错误（如 API Key 未设置）
            return fail(message=str(e), code=50001, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return fail(message=f'AI 服务异常：{str(e)}', code=50002, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema_view(
    post=extend_schema(
        summary='AI 多轮对话',
        description=(
            '带记忆的多轮对话接口。同一 session_id 共享对话历史，AI 能记住上下文。\n\n'
            '示例流程：\n'
            '1. POST { "query": "海南中学哪年成立？", "session_id": "abc" }\n'
            '2. POST { "query": "那它的校训是什么？", "session_id": "abc" }\n'
            '   → AI 知道"它"指海南中学'
        ),
        request=ChatWithMemorySerializer,
    ),
    delete=extend_schema(
        summary='清除会话记忆',
        description=(
            '清除指定 session_id 的对话历史。\n\n'
            '请求体：{ "session_id": "abc" }'
        ),
    ),
)
class ChatSessionView(APIView):
    """带记忆的多轮对话 —— 同一 session_id 共享上下文。"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatWithMemorySerializer(data=request.data)
        if not serializer.is_valid():
            return fail(message='参数校验失败', data=serializer.errors)

        query = serializer.validated_data['query']
        session_id = serializer.validated_data['session_id']

        try:
            answer = chat_with_memory(query, session_id)
            return ok(data={'answer': answer, 'session_id': session_id}, message='查询成功')
        except ValueError as e:
            return fail(message=str(e), code=50001, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return fail(message=f'AI 服务异常：{str(e)}', code=50002, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        session_id = request.data.get('session_id', '')
        if not session_id:
            return fail(message='session_id 不能为空')

        cleared = clear_session(session_id)
        if cleared:
            return ok(message=f'已清除会话 {session_id} 的记忆')
        return fail(message=f'会话 {session_id} 不存在或已过期', code=40401)
