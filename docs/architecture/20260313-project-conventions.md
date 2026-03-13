# 项目规约：Python AI Agent 实践

**日期**: 2026-03-13  
**适用范围**: 本仓库内所有实验脚本、shared 模块及协作开发。

---

## 1. 项目定位

本仓库为 **Python AI Agent 实践项目**，按主题进行实验（CrewAI、提示词、RAG 等）。所有实验共用同一虚拟环境与共享代码，需统一约定以保持可维护性与可复现性。

---

## 2. 统一日志与打印

### 2.1 使用标准库 logging，禁止散落 print

- **所有输出**（进度、结果、错误、调试信息）一律通过 `logging` 完成，不使用裸 `print()` 做业务输出。
- 脚本入口处应**先配置日志**再执行业务逻辑，推荐使用 `shared.logging_config.setup_logging()` 统一格式与级别。
- 模块内使用 `logger = logging.getLogger(__name__)`，通过 `logger.info()` / `logger.debug()` / `logger.warning()` / `logger.error()` 输出。

### 2.2 统一日志格式

- 格式建议：`%(asctime)s [%(levelname)s] %(name)s: %(message)s`，便于排查与复现。
- 默认级别：`INFO`；调试时可设为 `DEBUG`（通过环境变量或参数控制，不写死）。
- 敏感信息（API Key、Token、密码、完整用户输入等）**不得**写入日志。

### 2.3 与 LLM 调用日志的关系

- 模型调用过程由 `shared.llm` 中的 callback（如 `LLMCallbacksLogger`）统一写日志（调用开始/结束/异常、可选请求预览）。
- 业务脚本只负责配置根 logger，无需重复实现 LLM 调用日志。

---

## 3. 使用公共工具（shared）

### 3.1 模型调用与 LLM 配置

- **模型调用与配置**必须通过 `shared` 提供的入口，不在各实验脚本中硬编码 API 地址、Key 或重复实现调用逻辑。
- **LangChain 场景**：使用 `shared.llm.aliyun_llm.get_aliyun_llm()` / `get_openai_llm()` 获取 LLM 实例，已内置日志 callback。
- **CrewAI 等非 LangChain 场景**：使用 `shared.llm.aliyun_llm.get_aliyun_llm_env()` 获取环境配置，再传入框架的 LLM 类（如 `crewai.LLM(**get_aliyun_llm_env())`）。
- 环境变量由项目根目录 `.env` 统一管理（如 `DASHSCOPE_API_KEY`、`OPENAI_API_KEY`）；脚本中通过 `load_dotenv(project_root / ".env")` 加载，不散落 key。

### 3.2 工具与能力

- 自定义工具（如百度搜索）统一放在 **`shared/tools`**，通过 `from shared.tools import ...` 使用。
- 新增通用工具时在 `shared/tools` 下实现并在 `shared/tools/__init__.py` 中导出，实验脚本只做引用，不复制实现。

### 3.3 路径与入口

- 实验脚本需将**项目根目录**加入 `sys.path`，以便稳定导入 `shared`（例如 `Path(__file__).resolve().parent.parent.parent` 作为 project_root 并 `sys.path.insert(0, str(project_root))`）。
- `.env` 从项目根加载：`load_dotenv(project_root / ".env")`。

---

## 4. 规约小结

| 项 | 要求 |
|----|------|
| 输出方式 | 统一用 `logging`，不用裸 `print` 做业务输出 |
| 日志配置 | 使用 `shared.logging_config.setup_logging()` 或同等格式/级别 |
| 模型调用 | 使用 `shared.llm` 的 `get_aliyun_llm` / `get_aliyun_llm_env` / `get_openai_llm` |
| 工具与能力 | 使用 `shared.tools` 的公共工具，不重复造轮子 |
| 环境变量 | 根目录 `.env` + `load_dotenv(project_root / ".env")` |
| 敏感信息 | 不写入日志、不提交仓库 |

---

## 5. 参考文件

- 统一日志配置：`shared/logging_config.py`
- LLM 与调用日志：`shared/llm/aliyun_llm.py`
- 公共工具导出：`shared/tools/__init__.py`
- 示例脚本：`experiments/01-crewai-react-agent/scripts/03-full-example.py`
