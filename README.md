# LangChain + CrewAI 学习仓库

按「阶段 + 课程」组织（Phase + L），公共 LLM 与工具放在一级目录，便于按阶段学习 LangChain、RAG、向量数据库、CrewAI、AI 编程工具与大模型基础，并支持后续扩展新课。

---

## 课程简介 / 你将获得

- **面向**：希望系统学习 AI 应用开发、Agent、RAG 与多智能体协作的开发者。
- **内容**：大模型基础与环境、LangChain（链/Agent/RAG）、向量数据库与 RAG 进阶、CrewAI 多智能体、OpenClaw 与 Claude Code 实战、可观测与生产实践。
- **结构**：所有课程按阶段平铺（Phase1L1、Phase2L1…），`llm/` 与 `tools/` 为根目录公共依赖，各课复用。

---

## 学习路径（阶段与课程）

| 阶段 | 目录 | 主题 |
|------|------|------|
| **Phase1 基础与认知** | Phase1L1_env_and_llm | 环境与 LLM 接入 |
| | Phase1L2_llm_basics | 大模型基础（Token、Prompt、Function Calling） |
| | Phase1L3_ai_coding_tools | AI 编程工具（Cursor、Claude Code） |
| **Phase2 LangChain** | Phase2L1_lcel_chain | LCEL 与链 |
| | Phase2L2_agent_tools | Agent 与工具 |
| | Phase2L3_rag_intro | RAG 入门 |
| **Phase3 向量与 RAG** | Phase3L1_vector_db | 向量数据库 |
| | Phase3L2_rag_advanced | RAG 进阶与检索策略 |
| **Phase4 CrewAI** | Phase4L1_agent_task_crew | Agent、Task、Crew |
| | Phase4L2_tools_mcp | 工具与 MCP |
| | Phase4L3_knowledge_memory | 知识库与记忆 |
| **Phase5 实战** | Phase5L1_openclaw | OpenClaw 实战 |
| | Phase5L2_claude_code | Claude Code / Cursor 实战 |
| **Phase6 生产与拓展** | Phase6L1_observability_eval | 可观测与评估 |
| | Phase6L2_langgraph_others | LangGraph 与其他框架 |

更细的技术与框架对照见：[docs/architecture/20260313-ai-dev-phased-learning-landscape.md](docs/architecture/20260313-ai-dev-phased-learning-landscape.md)。

---

## 项目结构

```
wensi_ai_practise/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
│
├── llm/                    # 公共：大模型封装（一级目录）
├── tools/                  # 公共：通用工具（一级目录）
├── docs/
│   └── architecture/       # 架构与学习路径文档
│
├── Phase1L1_env_and_llm/
├── Phase1L2_llm_basics/
├── Phase1L3_ai_coding_tools/
├── Phase2L1_lcel_chain/
├── Phase2L2_agent_tools/
├── Phase2L3_rag_intro/
├── Phase3L1_vector_db/
├── Phase3L2_rag_advanced/
├── Phase4L1_agent_task_crew/
├── Phase4L2_tools_mcp/
├── Phase4L3_knowledge_memory/
├── Phase5L1_openclaw/
├── Phase5L2_claude_code/
├── Phase6L1_observability_eval/
└── Phase6L2_langgraph_others/
```

- **llm/**：公共大模型封装，各课从此引用。
- **tools/**：公共工具（搜索、读写等），各课按需引用。
- **Phase{N}L{m}_***：第 N 阶段第 m 课，目录内为该课脚本、Notebook 及本课说明。

---

## 快速开始

- **环境**：Python 3.10+，建议使用虚拟环境。
- **安装**：`pip install -r requirements.txt`（或按项目说明使用 uv/poetry）。
- **配置**：复制 `.env.example` 为 `.env`，填写 API Key（如 OpenAI、通义等）。
- **运行示例**：在仓库根目录执行，例如 `cd Phase1L1_env_and_llm && python main.py`（具体以各课 README 为准）。

---

## 各课说明

| 课 | 学习目标 | 运行方式（示例） |
|----|----------|------------------|
| Phase1L1 | 完成环境与 LLM 首次调用 | 见课内 README |
| Phase1L2 | 理解 Token、Prompt、Function Calling | 见课内 README |
| Phase1L3 | 使用 Cursor/Claude Code 与规则、Skills | 见课内 README |
| Phase2L1 | 掌握 LCEL 与链式调用 | 见课内 README |
| Phase2L2 | 单 Agent + Tools、ReAct | 见课内 README |
| Phase2L3 | 文档加载、切分、向量化、简单 RAG 链 | 见课内 README |
| Phase3L1 | 使用一种向量库（Chroma/FAISS/pgvector） | 见课内 README |
| Phase3L2 | 检索策略、RAG 评估与调优 | 见课内 README |
| Phase4L1 | CrewAI Agent/Task/Crew 编排 | 见课内 README |
| Phase4L2 | 自定义工具与 MCP 集成 | 见课内 README |
| Phase4L3 | 知识库与记忆（Short/Long-term） | 见课内 README |
| Phase5L1 | OpenClaw 多 Agent 助手实战 | 见课内 README |
| Phase5L2 | Cursor Agent / Claude Code 做小项目 | 见课内 README |
| Phase6L1 | 可观测、Trace、Eval | 见课内 README |
| Phase6L2 | LangGraph、LlamaIndex 等对比与选型 | 见课内 README |

每课目录下可包含 `README.md` 与入口脚本（如 `main.py`），以课内说明为准。

---

## 常见问题

- **依赖安装失败**：确认 Python 版本与 `requirements.txt`，必要时使用虚拟环境。
- **API Key 未配置**：检查 `.env` 或环境变量，变量名参考 `.env.example`。
- **找不到 `llm` / `tools` 模块**：在仓库根目录执行脚本，或使用 `pip install -e .` 将当前仓库安装为可编辑包后再运行。

---

## 参考资源

- [LangChain 文档](https://python.langchain.com/)
- [CrewAI 文档](https://docs.crewai.com/)
- [LangChain RAG 教程](https://python.langchain.com/docs/tutorials/rag/)
- [kid0317/crewai_mas_demo](https://github.com/kid0317/crewai_mas_demo)（企业级多智能体设计实战配套仓库）
