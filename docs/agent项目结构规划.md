apps/
└── agent/                 <-- 新建的 AI 助手模块
    ├── __init__.py
    ├── apps.py
    ├── urls.py            <-- 路由：例如 POST /api/agent/chat/
    ├── views.py           <-- 接收提问，调用 services 层，返回统一响应
    ├── models.py          <-- 【可选】如果你需要保存聊天记录，建 ChatSession 和 ChatMessage 表
    ├── serializers.py     <-- 校验前端传来的 prompt
    └── services/          <-- 🌟 核心：LangChain 逻辑存放地
        ├── __init__.py
        ├── llm.py         <-- 统一定义底层模型（如初始化 OpenAI 或 Gemini 模型实例）
        ├── memory.py      <-- 封装历史会话记忆逻辑（让 AI 记得上下文）
        ├── tools.py       <-- 自定义工具（比如“查询班级人数”的数据库查询工具）
        └── engine.py      <-- 组装 Agent 或 RAG 逻辑，对外暴露核心对话函数