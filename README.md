# wensi_ai_practise

AI 探索实践项目 - 按主题进行 AI 技术探索与尝试

## 项目规约

- **统一日志**：使用 `logging`，入口处调用 `shared.logging_config.setup_logging()`，禁止裸 `print` 做业务输出。
- **公共工具与 LLM**：模型调用与配置使用 `shared/llm`（如 `get_aliyun_llm`、`get_aliyun_llm_env`），工具使用 `shared/tools`。
- 详细规约见 [docs/architecture/20260313-project-conventions.md](docs/architecture/20260313-project-conventions.md)。

## 项目结构

```
wensi_ai_practise/
├── README.md                    # 项目说明
├── requirements.txt             # 公共 Python 依赖
├── .env.example                 # 环境变量模板
├── .env                         # 环境变量（需创建，不提交 git）
├── venv/                        # 公共虚拟环境（所有主题共用）
├── .cursor/rules/               # Cursor 项目规约（统一日志、shared 使用）
├── docs/                        # 文档目录
│   ├── architecture/            # 架构与项目规约
│   ├── retrospective/          # 复盘与总结
│   └── topics/                  # 各主题深度文档
├── experiments/                 # 实验代码
│   ├── 01-crewai-react-agent/  # 主题 1: CrewAI ReAct Agent
│   ├── 02-prompt-engineering/  # 主题 2: 提示词工程
│   └── ...                      # 更多主题...
└── shared/                      # 共享代码
    ├── logging_config.py        # 统一日志配置
    ├── tools/                   # 自定义工具（百度搜索等）
    └── llm/                     # LLM 配置（阿里云百炼等）
```

## 环境设置

### 1. 激活公共虚拟环境

所有实验主题共用同一个虚拟环境：

```bash
# 从项目根目录激活
source venv/bin/activate
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Key
```

### 3. 安装新依赖（如需要）

```bash
source venv/bin/activate
pip install <package-name>
pip freeze > requirements.txt
```

## 探索主题路线图

### 进行中
- [x] **01-crewai-react-agent** - CrewAI ReAct Agent
  - CrewAI 基础概念和架构
  - ReAct 范式实现
  - 工具调用机制

### 待探索
- [ ] **02-prompt-engineering** - 提示词工程
- [ ] **03-rag** - 检索增强生成
- [ ] **04-multi-agent** - 多 Agent 协作
- [ ] **05-fine-tuning** - 模型微调
- [ ] **06-multimodal** - 多模态

## 实验记录模板

每个实验目录包含：
```
experiments/0x-topic-name/
├── README.md          # 本主题说明与总结
├── notebooks/         # Jupyter notebooks
├── scripts/           # 可执行脚本
└── outputs/           # 输出结果（可选）
```

## 工作流

1. 选择一个主题，创建对应的 `experiments/0x-topic-name/` 目录
2. 编写实验代码和 notebook
3. 更新主题内的 README.md，记录学习心得
4. 定期在 `docs/retrospective/` 写阶段性复盘

---

*Start small, iterate fast.*
