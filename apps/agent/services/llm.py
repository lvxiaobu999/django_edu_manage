"""大模型初始化 —— 统一管理 LLM 实例，方便切换模型或调整参数。"""

import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_llm() -> ChatOpenAI:
    """返回配置好的 ChatOpenAI 实例。

    从环境变量读取：
        OPENAI_API_KEY    — OpenAI API 密钥（必须）
        OPENAI_BASE_URL   — API Base URL（可选，用于代理或兼容 API）
        LLM_MODEL         — 模型名称（默认 gpt-4o-mini）
        LLM_TEMPERATURE   — 温度参数（默认 0.3，保持回答稳定）
    """
    # 首次调用时打印 API Key 前缀便于排查问题
    api_key = os.getenv('OPENAI_API_KEY', '')
    if not api_key:
        raise ValueError('环境变量 OPENAI_API_KEY 未设置，请在 .env 文件中配置')

    return ChatOpenAI(
        model=os.getenv('LLM_MODEL', 'gpt-4o-mini'),
        temperature=float(os.getenv('LLM_TEMPERATURE', '0.3')),
        openai_api_key=api_key,
        base_url=os.getenv('OPENAI_BASE_URL') or None,
    )


def get_embeddings() -> OpenAIEmbeddings:
    """返回 OpenAI Embeddings 实例，用于 RAG 文档向量化。"""
    api_key = os.getenv('OPENAI_API_KEY', '')
    if not api_key:
        raise ValueError('环境变量 OPENAI_API_KEY 未设置，请在 .env 文件中配置')

    return OpenAIEmbeddings(
        model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
        openai_api_key=api_key,
        base_url=os.getenv('OPENAI_BASE_URL') or None,
    )
