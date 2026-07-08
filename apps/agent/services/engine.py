"""Agent 编排引擎 —— 组装 LLM、工具、记忆，对外暴露统一的对话入口。

核心函数：
    chat(query: str) -> str          — 单次对话（无记忆）
    chat_with_memory(query: str, session_id: str) -> str — 带记忆的多轮对话
"""

import logging

from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from apps.agent.services.llm import get_llm
from apps.agent.services.memory import get_memory
from apps.agent.services.tools import query_school_knowledge

logger = logging.getLogger(__name__)

# 系统提示词：定义 Agent 的行为边界和回答风格
SYSTEM_PROMPT = """你是海南中学的智能助手，专门回答关于海南中学的各类问题。

你的职责：
1. 回答学校的历史、校训、校区、办学特色等基本信息。
2. 对于学校知识库能覆盖的问题，使用 query_school_knowledge 工具查询后给出准确回答。
3. 对于超出学校知识范围的问题（如天气、新闻、编程等），礼貌地说明你只负责回答学校相关问题。

回答要求：
- 使用中文回答。
- 基于工具返回的知识库内容作答，不要编造信息。
- 如果知识库未覆盖某个问题，诚实告知，不要猜测。
- 回答简洁、清晰、结构化，适当使用 markdown 格式。"""

# 提示词模板
PROMPT = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name='chat_history', optional=True),
    ('human', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad'),
])


def _create_agent():
    """创建 Agent 实例（内部工厂函数）。"""
    llm = get_llm()
    tools = [query_school_knowledge]
    agent = create_openai_tools_agent(llm, tools, PROMPT)
    return agent


def chat(query: str) -> str:
    """单次对话 —— 不保留历史记忆，每次都是独立问答。

    参数：
        query (str): 用户的问题/输入

    返回：
        str: Agent 的最终回答文本
    """
    logger.info('收到用户提问：%s', query[:100])

    agent = _create_agent()
    executor = AgentExecutor(
        agent=agent,
        tools=[query_school_knowledge],
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5,          # 最多 5 轮工具调用，防止死循环
    )

    result = executor.invoke({'input': query})
    answer = result.get('output', '抱歉，处理你的问题时出现了错误，请稍后重试。')

    logger.info('Agent 回答完成，长度：%d 字符', len(answer))
    return answer


# 按 session_id 缓存 memory 实例（生产环境应使用 Redis 等外部存储）
_memory_store: dict = {}  # key: session_id, value: ConversationBufferWindowMemory


def chat_with_memory(query: str, session_id: str) -> str:
    """带记忆的多轮对话 —— 同一 session_id 共享上下文。

    参数：
        query (str):      用户的问题/输入
        session_id (str): 会话标识，同一会话的问题共享历史记录

    返回：
        str: Agent 的最终回答文本
    """
    logger.info('[session=%s] 收到提问：%s', session_id, query[:100])

    # 获取或创建该 session 的 memory
    if session_id not in _memory_store:
        _memory_store[session_id] = get_memory(k=10)
    memory = _memory_store[session_id]

    agent = _create_agent()
    executor = AgentExecutor(
        agent=agent,
        tools=[query_school_knowledge],
        memory=memory,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    result = executor.invoke({'input': query})
    answer = result.get('output', '抱歉，处理你的问题时出现了错误，请稍后重试。')

    logger.info('[session=%s] Agent 回答完成，长度：%d 字符', session_id, len(answer))
    return answer


def clear_session(session_id: str) -> bool:
    """清除指定会话的记忆。

    参数：
        session_id (str): 要清除的会话标识

    返回：
        bool: True 表示成功清除，False 表示该会话不存在
    """
    if session_id in _memory_store:
        del _memory_store[session_id]
        logger.info('已清除会话记忆：%s', session_id)
        return True
    return False
