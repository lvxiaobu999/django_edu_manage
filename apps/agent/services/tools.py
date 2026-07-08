"""自定义工具 —— 供 Agent 调用的能力单元。

包含：
    - 学校知识库检索工具（RAG）：基于 学校简介.md 的向量检索
    - 后续可扩展：数据库查询工具（如"查询班级人数"）等
"""

import logging
from pathlib import Path

from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from apps.agent.services.llm import get_embeddings

logger = logging.getLogger(__name__)

# 知识库文件路径
_KNOWLEDGE_FILE = Path(__file__).resolve().parent.parent / '学校简介.md'

# 全局向量存储实例（懒加载，只初始化一次）
_vectorstore: FAISS | None = None


def _get_vectorstore() -> FAISS:
    """懒加载学校知识库向量存储。

    首次调用时：
        1. 读取 学校简介.md
        2. 按标题 + 段落切分为文档块
        3. 向量化后存入内存 FAISS 索引
    后续调用直接返回缓存实例。
    """
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    logger.info('正在构建学校知识库向量索引...')

    # 1. 加载文档
    loader = TextLoader(str(_KNOWLEDGE_FILE), encoding='utf-8')
    documents = loader.load()

    # 2. 文本切分：以 markdown 标题为自然边界，chunk_size=500，重叠 80 字符
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=['\n## ', '\n### ', '\n#### ', '\n', '。', '，', ' '],
    )
    docs = text_splitter.split_documents(documents)

    # 3. 向量化 + 存入 FAISS
    embeddings = get_embeddings()
    _vectorstore = FAISS.from_documents(docs, embeddings)

    logger.info('学校知识库向量索引构建完成，共 %d 个文档块', len(docs))
    return _vectorstore


@tool
def query_school_knowledge(question: str) -> str:
    """查询海南中学的学校历史、校训、校区、制度等静态知识。

    适用场景：
        - 学校成立年份、创办时间
        - 校训、办学理念
        - 校区分布与规模
        - 历史沿革
        - 校长、党委书记等基础信息

    参数：
        question (str): 关于学校的问题，建议用完整句式（如"海南中学是哪一年成立的？"）

    返回：
        str: 从学校知识库中检索到的相关内容。如果知识库中无相关信息，会明确说明。
    """
    try:
        vectorstore = _get_vectorstore()
        # 检索最相关的 3 个文档块
        docs = vectorstore.similarity_search(question, k=3)

        if not docs:
            return '学校知识库中暂未找到相关信息。'

        results = []
        for i, doc in enumerate(docs, 1):
            results.append(f'【来源片段 {i}】\n{doc.page_content.strip()}')

        return '\n\n'.join(results)

    except FileNotFoundError:
        return '错误：学校知识库文件（学校简介.md）不存在，请联系管理员。'
    except Exception as e:
        logger.exception('查询学校知识库失败')
        return f'查询知识库时发生错误：{str(e)}'
