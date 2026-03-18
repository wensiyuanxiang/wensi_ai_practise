"""
LlamaIndex 专用：阿里云通义千问 LLM 实现

基于阿里云 OpenAI 兼容接口，使用 LlamaIndex OpenAILike 封装。
"""
from __future__ import annotations

import logging
import os
from typing import Any

from llama_index.llms.openai_like import OpenAILike


def _get_logger():
    """获取模块级 logger。"""
    logger = logging.getLogger("llm.llamaindex_aliyun_llm")
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


class LlamaIndexAliyunLLM:
    """阿里云通义千问 LLM 类（LlamaIndex 专用）。"""

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
            **kwargs: 其他传递给 OpenAILike 的参数
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
        self.api_base = self.ENDPOINTS[region]

        self._llm = OpenAILike(
            model=self.model,
            api_key=self.api_key,
            api_base=self.api_base,
            temperature=self.temperature,
            timeout=self.timeout,
            max_tokens=self.max_tokens,
            is_chat_model=True,
            **kwargs,
        )

    def as_llamaindex(self) -> OpenAILike:
        """获取底层 LlamaIndex OpenAILike 实例。"""
        return self._llm

    def complete(self, *args: Any, **kwargs: Any) -> Any:
        """文本补全。"""
        return self._llm.complete(*args, **kwargs)

    async def acomplete(self, *args: Any, **kwargs: Any) -> Any:
        """异步文本补全。"""
        return await self._llm.acomplete(*args, **kwargs)

    def chat(self, *args: Any, **kwargs: Any) -> Any:
        """聊天对话。"""
        return self._llm.chat(*args, **kwargs)

    async def achat(self, *args: Any, **kwargs: Any) -> Any:
        """异步聊天对话。"""
        return await self._llm.achat(*args, **kwargs)

    def stream_complete(self, *args: Any, **kwargs: Any) -> Any:
        """流式文本补全。"""
        return self._llm.stream_complete(*args, **kwargs)

    async def astream_complete(self, *args: Any, **kwargs: Any) -> Any:
        """异步流式文本补全。"""
        return await self._llm.astream_complete(*args, **kwargs)

    def stream_chat(self, *args: Any, **kwargs: Any) -> Any:
        """流式聊天对话。"""
        return self._llm.stream_chat(*args, **kwargs)

    async def astream_chat(self, *args: Any, **kwargs: Any) -> Any:
        """异步流式聊天对话。"""
        return await self._llm.astream_chat(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """代理到底层 OpenAILike 实例。"""
        return getattr(self._llm, name)


# 便捷函数
def create_llamaindex_aliyun_llm(
    model: str = "qwen-plus",
    api_key: str | None = None,
    region: str = "cn",
    temperature: float | None = None,
    timeout: int = 600,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> LlamaIndexAliyunLLM:
    """创建 LlamaIndexAliyunLLM 实例的便捷函数。"""
    return LlamaIndexAliyunLLM(
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

    llm = LlamaIndexAliyunLLM(model="qwen-plus", temperature=0.7)
    response = llm.complete("你好，请介绍一下你自己")
    ColoredPrint.red("------> 响应:", response.text)
