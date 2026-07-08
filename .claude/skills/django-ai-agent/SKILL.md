---
name: django-ai-agent
description: 当用户要求在 Django 项目中添加 AI 助手、集成 LangChain、开发 RAG（检索增强生成）或 Agent 功能时，触发此技能。
---

# 核心上下文 (Context)
当前项目是一个基于 Django 的教育后端管理系统 (`django_edu_manage`)。我们需要在其中构建一个专业的 AI Agent 模块，底层使用 LangChain 框架驱动。

# 架构规范 (Frameworks & Architecture)
1. **模块化设计**：所有的 AI 逻辑必须收敛在一个独立的应用中（如 `apps/agent`），不得污染现有业务代码。
2. **瘦视图，胖服务 (Thin Views, Fat Services)**：
   - `views.py`：仅负责接收 HTTP 请求、参数校验、调用 Service 层，以及统一封装标准的 JSON 响应。
   - `services/`：核心逻辑目录。大模型的初始化、LangChain 的 Chain/Agent 编排、Memory（记忆）管理、Tools（工具）定义以及 RAG 检索器，均需模块化地放在此目录下。
3. **接口规范**：生成的 API 必须返回结构化的 JSON 数据，以便与现代化企业级前端控制台（如基于 React 的 SPA）进行无缝的数据交互。

# agent目录结构 (Directory Structure)
```text
apps/
└── agent/                 <-- 新建的 AI 助手模块
    ├── __init__.py
    ├── apps.py
    ├── urls.py            <-- 路由：例如 POST /api/agent/chat/
    ├── views.py           <-- 接收提问，调用 services 层，返回统一响应
    ├── models.py          <-- 【可选】如果你需要保存聊天记录，建 ChatSession 和 ChatMessage 表
    ├── serializers.py     <-- 校验前端传来的 prompt
    ├── 学校简介.md         <-- 学校历史、规章制度等静态知识库（RAG）文档
    └── services/          <-- 🌟 核心：LangChain 逻辑存放地
        ├── __init__.py
        ├── llm.py         <-- 统一定义底层模型（如初始化 OpenAI 或 Gemini 模型实例）
        ├── memory.py      <-- 封装历史会话记忆逻辑（让 AI 记得上下文）
        ├── tools.py       <-- 自定义工具（比如“查询班级人数”的数据库查询工具）
        └── engine.py      <-- 组装 Agent 或 RAG 逻辑，对外暴露核心对话函数
```

# 开发决策点 (Decision Points)
- **依赖管理**：如果需要安装新包，请优先提示用户使用 `uv add <package>`（例如 `uv add langchain langchain-openai`）。
- **知识库 (RAG)**：如果需求涉及“学校历史”、“规章制度”等静态私有知识，必须采用 RAG 架构（Document Loader -> Text Splitter -> Vector Store -> Retriever）。
- **工具调用 (Tool Calling)**：如果需求涉及动态查询（例如“实时查询某个班级的人数”），请在 `services/tools.py` 中定义 LangChain `@tool`，并在 Agent 初始化时进行绑定。

# 反模式 (Anti-patterns - 绝对禁止)
- **严禁**在 `views.py` 或 `urls.py` 中直接写死大模型的 API Key。必须通过 `os.getenv` 或 `django.conf.settings` 从 `.env` 系列文件读取。
- **严禁**在 View 层直接实例化大模型或进行复杂的 Prompt 拼接。
- **严禁**生成阻塞主线程且没有超时机制的长耗时同步网络请求。

# 预期输出 (Output Expectations)
当你执行完代码生成后，请向用户简要汇报：
1. 创建/修改了哪些文件。
2. 需要向 `.env.development` 等配置文件中追加哪些环境变量。
3. 对应的 API 路由地址以及一段用于测试的 `curl` 示例命令。

