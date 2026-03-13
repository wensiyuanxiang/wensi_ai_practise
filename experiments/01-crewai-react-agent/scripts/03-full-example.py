#!/usr/bin/env python3
"""
完整示例：带百度搜索的网络调研专家 Agent
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 从项目根加载 .env，保证 DASHSCOPE_API_KEY / OPENAI_API_KEY 等可用
load_dotenv(project_root / ".env")

from crewai import Agent, Task, Crew, LLM
from crewai_tools import ScrapeWebsiteTool, FileWriterTool

# 使用 shared 公共工具与 LLM 配置
from shared.llm.aliyun_llm import get_aliyun_llm_env

baidu_search_tool = None
try:
    from shared.tools import baidu_search_tool as _baidu_search_tool
    baidu_search_tool = _baidu_search_tool
except ImportError:
    print("警告: 未找到 shared.tools 百度搜索工具，将仅使用基础工具")

# 初始化工具
scrape_tool = ScrapeWebsiteTool()
file_writer = FileWriterTool()

# 工具列表（含 shared 提供的百度搜索）
tools = [scrape_tool, file_writer]
if baidu_search_tool is not None:
    tools.append(baidu_search_tool)

# LLM：优先使用 shared 的阿里云百炼配置，否则 CrewAI 用 OPENAI_* 环境变量
aliyun_env = get_aliyun_llm_env()
llm = LLM(**aliyun_env) if aliyun_env else None

# 创建 Agent
researcher = Agent(
    role="网络调研专家",
    goal="通过系统化的网络搜索和信息提取，完成用户指定的调研任务，并生成结构化的 Markdown 调研报告",
    backstory="""你是一位经验丰富的网络调研专家，擅长通过系统化的方法收集、分析和整理网络信息。

你的工作流程：
1. **任务分析**：理解用户需求，明确调研目标
2. **搜索策略**：使用 BaiduSearchTool 进行关键词搜索
3. **深度挖掘**：对重要链接使用 ScrapeWebsiteTool 抓取完整内容
4. **信息整理**：结构化整理，验证信息准确性
5. **报告生成**：生成 Markdown 格式报告并使用 FileWriterTool 保存

注意：不要仅依赖搜索摘要，必须抓取原始网页内容！
""",
    tools=tools,
    llm=llm,
    verbose=True,
)

# 创建任务
task = Task(
    description="""调研主题：CrewAI 框架的核心概念和使用方法

要求：
1. 先搜索 CrewAI 相关信息
2. 找到官方文档链接并抓取内容
3. 了解 Agent、Task、Crew 等核心概念
4. 生成一份详细的调研报告，保存到 crewai_report.md
""",
    expected_output="一份完整的 Markdown 调研报告",
    agent=researcher,
    output_file="outputs/crewai_report.md"
)

# 创建 Crew 并运行
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=True
)

if __name__ == "__main__":
    # 确保输出目录存在（output_file 相对 cwd，通常为实验目录）
    outputs_dir = Path(__file__).resolve().parent.parent / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("CrewAI 网络调研专家")
    print("=" * 60)
    print(f"可用工具: {[t.name for t in tools]}")
    print()

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("调研完成！")
    print("=" * 60)
    print(result)
