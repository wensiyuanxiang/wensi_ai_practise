"""
LangGraph 专用：阿里云通义千问 LLM 实现

基于 LangChainAliyunLLM，提供 LangGraph 常用的便捷方法。
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional, Sequence, Union

from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool

from .langchain_aliyun_llm import LangChainAliyunLLM


def _get_logger():
    """获取模块级 logger。"""
    logger = logging.getLogger("llm.langgraph_aliyun_llm")
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


class LangGraphAliyunLLM(LangChainAliyunLLM):
    """阿里云通义千问 LLM 类（LangGraph 专用）。"""

    def __init__(
        self,
        model: str = "qwen-plus",
        api_key: str | None = None,
        region: str = "cn",
        temperature: float | None = None,
        timeout: int = 600,
        max_tokens: int | None = None,
        tools: Sequence[Union[Dict[str, Any], BaseTool]] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        初始化 LangGraph 阿里云 LLM。

        Args:
            model: 模型名称，如 "qwen-plus", "qwen-turbo", "qwen-max" 等
            api_key: API Key，不提供则从环境变量 ALIYUN_API_KEY 或 DASHSCOPE_API_KEY 读取
            region: 地域 "cn" / "intl" / "finance"
            temperature: 采样温度
            timeout: 请求超时（秒），默认 600
            max_tokens: 最大生成 Token 数
            tools: 要绑定的工具列表
            **kwargs: 其他传递给 ChatOpenAI 的参数
        """
        super().__init__(
            model=model,
            api_key=api_key,
            region=region,
            temperature=temperature,
            timeout=timeout,
            max_tokens=max_tokens,
            **kwargs,
        )

        if tools:
            self.bind_tools(tools)

    def as_runnable(self) -> Runnable:
        """获取 LangChain Runnable 实例，用于 LangGraph 集成。"""
        return self._llm

    def create_agent_node(
        self,
        _name: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        """
        创建 LangGraph StateGraph 节点函数。

        Args:
            _name: 节点名称（未使用，保留兼容）
            system_prompt: 系统提示词

        Returns:
            LangGraph 节点函数
        """
        return create_agent_node(self._llm, system_prompt=system_prompt)

    def should_continue(self, state: Dict[str, Any]) -> str:
        """
        LangGraph 条件边：判断是否需要继续工具调用。

        Args:
            state: 当前状态

        Returns:
            "tools" 或 "end"
        """
        return should_continue(state)


def create_agent_node(
    llm: Runnable,
    _name: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    创建 LangGraph StateGraph 节点函数。

    Args:
        llm: LLM 实例
        _name: 节点名称（未使用，保留兼容）
        system_prompt: 系统提示词

    Returns:
        LangGraph 节点函数
    """
    def agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
        messages = state.get("messages", [])

        if system_prompt:
            if messages and isinstance(messages[0], SystemMessage):
                messages = [SystemMessage(content=system_prompt)] + messages[1:]
            else:
                messages = [SystemMessage(content=system_prompt)] + messages

        response = llm.invoke(messages)
        return {"messages": [response]}

    return agent_node


def should_continue(state: Dict[str, Any]) -> str:
    """
    LangGraph 条件边：判断是否需要继续工具调用。

    Args:
        state: 当前状态

    Returns:
        "tools" 或 "end"
    """
    messages = state.get("messages", [])
    if not messages:
        return "end"

    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return "end"


# 便捷函数
def create_aliyun_langgraph_llm(
    model: str = "qwen-plus",
    api_key: str | None = None,
    region: str = "cn",
    temperature: float | None = None,
    timeout: int = 600,
    max_tokens: int | None = None,
    tools: Sequence[Union[Dict[str, Any], BaseTool]] | None = None,
    **kwargs: Any,
) -> LangGraphAliyunLLM:
    """创建 LangGraphAliyunLLM 实例的便捷函数。"""
    return LangGraphAliyunLLM(
        model=model,
        api_key=api_key,
        region=region,
        temperature=temperature,
        timeout=timeout,
        max_tokens=max_tokens,
        tools=tools,
        **kwargs,
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    _root = Path(__file__).resolve().parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    from tools import ColoredPrint

    llm = LangGraphAliyunLLM(model="qwen-plus", temperature=0.7)
    response = llm.invoke("你好，请介绍一下你自己")
    ColoredPrint.red("------> 响应:", response.content)
