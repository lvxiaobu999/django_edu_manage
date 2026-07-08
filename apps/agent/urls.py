"""AI Agent 路由配置。

接口：
    POST   /api/agent/chat/           — 单次问答
    POST   /api/agent/chat/session/   — 带记忆的多轮对话
    DELETE /api/agent/chat/session/   — 清除会话记忆
"""

from django.urls import path

from apps.agent.views import ChatView, ChatSessionView

urlpatterns = [
    path('agent/chat', ChatView.as_view(), name='agent-chat'),
    path('agent/chat/session', ChatSessionView.as_view(), name='agent-chat-session'),
]
