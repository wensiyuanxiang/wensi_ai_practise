"""
LangChain 专用：阿里云通义千问 LLM 实现

基于阿里云 OpenAI 兼容接口，使用 LangChain ChatOpenAI 封装。
"""
from __future__ import annotations

import logging
import os
from typing import Any

from langchain_openai import ChatOpenAI


def _get_logger():
    """获取模块级 logger。"""
    logger = logging.getLogger("llm.langchain_aliyun_llm")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


logger = _get_logger()


class LangChainAliyunLLM:
    """阿里云通义千问 LLM 类（LangChain 专用）。"""

    ENDPOINTS = {
        "cn": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "intl": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "finance": "https://dashscope-finance.aliyuncs.com/compatible-mode/v1",
    }

    def __init__(
        self,
        model: str = "qwen-plus",
        api_key: str | None = None,
        region: str = "cn",
        temperature: float | None = None,
        timeout: int = 600,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        初始化阿里云 LLM。

        Args:
            model: 模型名称，如 "qwen-plus", "qwen-turbo", "qwen-max" 等
            api_key: API Key，不提供则从环境变量 ALIYUN_API_KEY 或 DASHSCOPE_API_KEY 读取
            region: 地域 "cn" / "intl" / "finance"
            temperature: 采样温度
            timeout: 请求超时（秒），默认 600
            max_tokens: 最大生成 Token 数
            **kwargs: 其他传递给 ChatOpenAI 的参数
        """
        self.model = model
        self.region = region
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens

        self.api_key = api_key or os.getenv("ALIYUN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 未提供。请通过 api_key 传入或设置环境变量 ALIYUN_API_KEY 或 DASHSCOPE_API_KEY"
            )

        if region not in self.ENDPOINTS:
            raise ValueError(f"不支持的地域: {region}，支持: {list(self.ENDPOINTS.keys())}")
        self.base_url = self.ENDPOINTS[region]

        self._llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            timeout=self.timeout,
            max_tokens=self.max_tokens,
            **kwargs,
        )

    def as_langchain(self) -> ChatOpenAI:
        """获取底层 LangChain ChatOpenAI 实例。"""
        return self._llm

    def bind_tools(self, tools: list, **kwargs: Any) -> "LangChainAliyunLLM":
        """绑定工具。"""
        self._llm = self._llm.bind_tools(tools, **kwargs)
        return self

    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        """调用 LLM。"""
        return self._llm.invoke(*args, **kwargs)

    async def ainvoke(self, *args: Any, **kwargs: Any) -> Any:
        """异步调用 LLM。"""
        return await self._llm.ainvoke(*args, **kwargs)

    def stream(self, *args: Any, **kwargs: Any) -> Any:
        """流式调用 LLM。"""
        return self._llm.stream(*args, **kwargs)

    async def astream(self, *args: Any, **kwargs: Any) -> Any:
        """异步流式调用 LLM。"""
        return await self._llm.astream(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """代理到底层 ChatOpenAI 实例。"""
        return getattr(self._llm, name)


# 便捷函数
def create_langchain_aliyun_llm(
    model: str = "qwen-plus",
    api_key: str | None = None,
    region: str = "cn",
    temperature: float | None = None,
    timeout: int = 600,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> LangChainAliyunLLM:
    """创建 LangChainAliyunLLM 实例的便捷函数。"""
    return LangChainAliyunLLM(
        model=model,
        api_key=api_key,
        region=region,
        temperature=temperature,
        timeout=timeout,
        max_tokens=max_tokens,
        **kwargs,
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from tools import ColoredPrint

    llm = LangChainAliyunLLM(model="qwen-plus", temperature=0.7)
    response = llm.invoke("你好，请介绍一下你自己")
    ColoredPrint.red("------> 响应:", response.content)
