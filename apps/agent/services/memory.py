"""对话记忆管理 —— 让 Agent 在多轮对话中记住上下文。"""

from langchain_classic.memory import ConversationBufferWindowMemory


def get_memory(k: int = 10) -> ConversationBufferWindowMemory:
    """创建滑动窗口对话记忆。

    参数：
        k (int): 保留最近 k 轮对话。默认 10 轮，平衡上下文长度和 API 费用。

    返回：
        ConversationBufferWindowMemory：配置了滑动窗口的记忆实例。

    说明：
        - memory_key='chat_history' 是 LangChain Agent 的默认键名
        - return_messages=True 确保返回 Message 对象而非纯字符串
        - 每次对话独立创建 memory 实例，不同用户/会话之间隔离
    """
    return ConversationBufferWindowMemory(
        k=k,
        memory_key='chat_history',
        return_messages=True,
    )
