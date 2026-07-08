"""AI Agent 序列化器 —— 校验前端传入的请求参数。"""

from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    """单次对话请求。

    POST /api/agent/chat/
        { "query": "海南中学是哪一年成立的？" }
    """
    query = serializers.CharField(
        required=True,
        max_length=2000,
        help_text='用户提问内容，最多 2000 字符',
    )


class ChatWithMemorySerializer(serializers.Serializer):
    """带记忆的多轮对话请求。

    POST /api/agent/chat/session/
        {
            "query": "它的校训是什么？",
            "session_id": "abc-123"
        }
    """
    query = serializers.CharField(
        required=True,
        max_length=2000,
        help_text='用户提问内容，最多 2000 字符',
    )
    session_id = serializers.CharField(
        required=True,
        max_length=128,
        help_text='会话标识，同一会话共享对话历史',
    )
