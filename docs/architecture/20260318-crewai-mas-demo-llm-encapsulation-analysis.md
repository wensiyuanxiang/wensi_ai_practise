# crewai_mas_demo llm 封装分析与借鉴

日期：2026-03-18  
目的：学习 [kid0317/crewai_mas_demo](https://github.com/kid0317/crewai_mas_demo) 仓库中 `llm/` 目录的封装方式，归纳其针对 CrewAI + 阿里云通义的适配与改造，供本仓库 llm 模块演进参考。

---

## 一、整体定位

- **继承**：`AliyunLLM(BaseLLM)`，完全兼容 CrewAI 的 Agent / Task / Crew 调用链。
- **目标**：在不依赖 OpenAI API 的前提下，用阿里云 DashScope（通义）兼容接口驱动 CrewAI。
- **入口**：`llm/__init__.py` 导出 `AliyunLLM`，各 Phase 课程或 Agent 直接 `from llm import AliyunLLM` 使用。

---

## 二、核心适配与改造

### 1. 多地域与端点

- **ENDPOINTS** 字典支持三地域：
  - `cn`：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
  - `intl`：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`
  - `finance`：`https://dashscope-finance.aliyuncs.com/compatible-mode/v1/chat/completions`
- 构造时传入 `region`，校验后写入 `self.endpoint`，请求统一走 compatible-mode，与 OpenAI 报文格式一致。

### 2. 多模态消息归一化（CrewAI 工具 → DashScope）

- **问题**：CrewAI 的 AddImageTool / AddImageToolLocal 会把“图片”以工具结果形式写进 **assistant 消息的 content 字符串**（如 "Add image to content Local ... data:image/...;base64,..." 或 "Observation: http..."）。DashScope 期望的是 **user 消息 + 多模态 content 数组**，否则易 400 或体积超限。
- **改造**：`_normalize_multimodal_tool_result(messages)`：
  - 遍历消息，若为 assistant 且 content 为字符串；
  - 若包含 "Add image to content Local" 且带 `data:image/...;base64,`，则从 content 中抽出 data URL，构造一条 **user 消息**，`content` 为 `[{ "type": "text", "text": "..." }, { "type": "image_url", "image_url": { "url": data_url } }]`；
  - 若为 "Observation: http..." 形式，则构造 `"type": "image", "image": url` 的 user 多模态消息；
  - 返回 `(处理后 messages, 是否使用多模态)`；若为多模态，后续请求将 **model 替换为 image_model**（默认 `qwen3-vl-plus`）。

这样 CrewAI 侧无需改工具，仅 LLM 层做一次“工具结果 → 多模态 user 消息”的转换，兼容 DashScope。

### 3. 重试策略

- **网络/服务异常**：对 5xx、429、Timeout、RequestException 做重试。重试次数 `retry_count` 默认 2，可由环境变量 `LLM_RETRY_COUNT` 覆盖。
- **空内容重试**：若模型返回的 `content` 为空字符串（常见于限流或偶发），则递归 `call` 再试，最多 2 次（`_empty_retry_count`），超过后抛错，避免无限递归。

### 4. Function Calling 与 CrewAI 分工

- **supports_function_calling()** 返回 `True`，请求体可带 `tools`。
- 若响应含 `tool_calls`：
  - **有** `available_functions`：在本层执行 `_handle_function_calls`，将 tool 结果追加为 `role: "tool"` 消息后递归 `call`，直到模型返回文本或达到 `max_iterations`。
  - **无** `available_functions`（CrewAI executor 故意传 `None`）：不执行工具，直接 **返回 `message["tool_calls"]`**，由 CrewAI 的 `_handle_native_tool_calls` 等上层逻辑执行。这样既支持“LLM 内执行工具”，也支持“交给 CrewAI 执行”两种用法。

### 5. Stop words 与上下文长度

- **supports_stop_words()** 返回 `True`，`_prepare_stop_words` 将 CrewAI 的 stop 配置转为 API 的 `stop` 参数。
- **get_context_window_size()**：根据 `model` 名称简单规则（如含 "long" 则 200_000，否则 8192），供框架做上下文裁剪或提示。

### 6. 异步与回调

- **acall**：用 `asyncio.to_thread` 包装同步 `call`，满足 CrewAI 异步接口，不阻塞事件循环。
- **callbacks**：在 `call` 内按需调用 `on_llm_start(messages)`、`on_llm_end(result)`，便于 LangSmith/LangTrace 等可观测集成。

### 7. 消息校验

- **\_validate_messages**：校验每条消息的 `role`（system/user/assistant/tool）、`content` 或 `tool_calls`、tool 消息的 `tool_call_id` 等，多模态下允许 `content` 为 list（text + image_url/image），避免非法报文直接打到 API。

### 8. 配置与环境

- **API Key**：优先构造函数参数 `api_key`，否则 `QWEN_API_KEY`，再否则 `DASHSCOPE_API_KEY`。
- **timeout**：默认 600 秒，适合长上下文或多轮 Function Calling。
- **image_model**：多模态时替换的模型，默认 `qwen3-vl-plus`，可构造时传入覆盖。

---

## 三、测试与工程化

- **pytest**：`test_aliyun_llm.py` 对 `__init__`、`call`、重试、Function Calling、空内容重试、多地域等做单测，目标高覆盖率；`test_aliyun_llm_integration.py` 做集成；`test_multimodal_message.py` 专门测多模态格式与 `_validate_messages`。
- **requirements-test.txt**：测试依赖与 pytest 配置（如 `pytest.ini`）独立，便于 CI 只装测试依赖。

---

## 四、本仓库可借鉴点

| 项目 | 建议 |
|------|------|
| **BaseLLM 兼容** | 若以 CrewAI 为主线，可同样继承 `BaseLLM`，实现 `call` / `acall` 及 `supports_*`，保证 Agent/Task 无感切换。 |
| **多模态** | 若有“上传图片”类工具，可借鉴“工具结果 → 多模态 user 消息”的归一化逻辑，避免 DashScope 400。 |
| **多地域** | 若需 intl/finance，可抽象 endpoint 表 + `region` 参数。 |
| **重试与空内容** | 统一重试次数与空内容重试上限，减少偶发失败。 |
| **Function Calling 分工** | 明确“有 available_functions 时自执行、无时返回 tool_calls”的语义，与 CrewAI executor 约定一致。 |
| **测试** | 对重试、多地域、多模态、tool_calls 分支做单测与少量集成测，保证后续改动能回归。 |

---

## 五、参考链接

- 仓库 llm 目录：[crewai_mas_demo/llm](https://github.com/kid0317/crewai_mas_demo/tree/main/llm)
- 核心实现：`aliyun_llm.py`（BaseLLM、call、acall、多模态归一化、重试、Function Calling）
- 测试：`test_aliyun_llm.py`、`test_multimodal_message.py`
