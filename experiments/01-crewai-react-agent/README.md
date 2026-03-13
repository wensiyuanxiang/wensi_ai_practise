# CrewAI ReAct Agent

> 使用 crewAI 实现 ReAct 范式的测试 Agent

## 主题概述

探索 CrewAI 框架，实现基于 ReAct（Reasoning + Acting）范式的智能 Agent，学习如何构建能够思考、行动和观察的自主代理。

## 学习目标

- [ ] 了解 CrewAI 基础概念和架构
- [ ] 实现一个基础的 ReAct 模式 Agent
- [ ] 学习 Agent 工具调用机制
- [ ] 理解 Task 和 Crew 的组织方式

## 实验内容

### 实验 1: 网络调研专家 Agent

**文件**: `scripts/01-web-research-agent.py`

**描述**: 完整的网络调研专家 Agent，包含：
- 系统化的调研工作流程
- 网页抓取工具 (ScrapeWebsiteTool)
- 文件读写工具 (FileWriterTool, FileReadTool)
- 结构化 Markdown 报告生成

**使用方式**:
```bash
cd experiments/01-crewai-react-agent
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 API Key
python scripts/01-web-research-agent.py
```

### 实验 2: 简化版示例

**文件**: `scripts/02-simple-example.py`

**描述**: 最小化的 CrewAI 使用示例，适合快速上手

### 配置文件

- `requirements.txt` - Python 依赖
- `.env.example` - 环境变量模板

## 总结与收获

在此记录本次主题学习的关键收获、遇到的坑、最佳实践等。

## 参考资料

- [CrewAI 官方文档](https://docs.crewai.com/)
- [ReAct 论文](https://arxiv.org/abs/2210.03629)
