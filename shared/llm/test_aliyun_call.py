#!/usr/bin/env python3
"""
验证阿里云 LLM 调用与 LLMCallbacksLogger 日志是否正常。
运行前请设置 DASHSCOPE_API_KEY 或 ALIYUN_API_KEY。
从项目根目录执行: python -m shared.llm.test_aliyun_call
或: python shared/llm/test_aliyun_call.py
"""

import logging
import sys
from pathlib import Path

# 项目根加入 path，便于 import shared
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dotenv import load_dotenv
load_dotenv(_root / ".env")

# 先配置日志再 import aliyun_llm，这样 logger 会使用这里的配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    from langchain_core.messages import HumanMessage

    from shared.llm.aliyun_llm import get_aliyun_llm

    logger.info("开始验证阿里云 LLM 与日志")
    llm = get_aliyun_llm(
        model="qwen-plus", temperature=0.3, max_tokens=64, log_prompts=True
    )
    messages = [HumanMessage(content="你好，请用一句话介绍你自己。")]
    logger.info("发起一次 invoke，观察上方/下方应出现 LLM 调用开始/结束日志")
    response = llm.invoke(messages)
    logger.info("调用完成，content 类型: %s", type(response).__name__)
    if hasattr(response, "content"):
        print("--- 模型回复 ---")
        print(response.content)
        print("---")
    else:
        print("--- 原始响应 ---")
        print(response)
        print("---")


if __name__ == "__main__":
    main()
