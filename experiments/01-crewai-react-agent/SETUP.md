# 环境设置指南

## 前置要求

- Python 3.10+ (已安装 Python 3.12)

## 快速开始

### 1. 激活项目公共虚拟环境

**所有实验主题共用同一个虚拟环境**，位于项目根目录：

```bash
# 从项目根目录激活
cd /path/to/wensi_ai_practise
source venv/bin/activate

# 或从任意实验目录激活
cd experiments/01-crewai-react-agent
source ../../venv/bin/activate
```

### 2. 配置 API Key

在项目根目录创建 `.env` 文件（所有主题共用）：

```bash
cd /path/to/wensi_ai_practise
cp experiments/01-crewai-react-agent/.env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```bash
# OpenAI（任选其一）
OPENAI_API_KEY=sk-xxx

# 或阿里云百炼
DASHSCOPE_API_KEY=sk-xxx
```

### 3. 运行示例

```bash
cd experiments/01-crewai-react-agent

# 确保已激活虚拟环境
source ../../venv/bin/activate

# 简单示例
python scripts/02-simple-example.py

# 完整示例（带百度搜索）
python scripts/03-full-example.py
```

## 公共虚拟环境说明

项目使用**单一公共虚拟环境**，位于：
```
wensi_ai_practise/venv/
```

**优点：**
- 所有实验主题共享依赖，无需重复安装
- 节省磁盘空间
- 统一管理依赖版本

**添加新依赖：**
```bash
# 激活虚拟环境
source venv/bin/activate

# 安装新包
pip install <package-name>

# 更新 requirements.txt
pip freeze > requirements.txt
```

## 已安装的包

```
crewai>=1.10.0
crewai-tools>=1.10.0
langchain>=1.0.0
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 项目结构

```
wensi_ai_practise/
├── venv/                    # 公共虚拟环境（所有主题共用）
├── requirements.txt        # 公共依赖列表
├── .env                     # 环境变量（所有主题共用，需创建）
├── shared/                  # 共享工具
│   ├── tools/
│   │   └── baidu_search.py      # 百度搜索工具
│   └── llm/
│       └── aliyun_llm.py        # 阿里云 LLM 配置
└── experiments/
    └── 01-crewai-react-agent/
        ├── scripts/             # Python 脚本
        │   ├── 01-web-research-agent.py
        │   ├── 02-simple-example.py
        │   └── 03-full-example.py
        ├── notebooks/          # Jupyter notebooks
        ├── outputs/            # 输出目录
        ├── .env.example       # 环境变量模板
        └── SETUP.md           # 本文件
```
