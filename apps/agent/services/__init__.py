"""AI Agent 服务层 —— LangChain 核心逻辑。

子模块：
    llm.py     — 大模型实例化（ChatOpenAI）
    tools.py   — 自定义工具（学校知识库检索、数据库查询等）
    memory.py  — 对话记忆管理
    engine.py  — Agent / RAG 编排，对外暴露统一调用入口
"""
