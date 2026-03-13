"""
阿里云百炼 LLM 配置
支持 Qwen 等模型
每次调用会通过 callback 将调用过程写入日志。
"""

import logging
import os
from typing import Any, Optional, cast

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

logger = logging.getLogger(__name__)


class LLMCallbacksLogger(BaseCallbackHandler):
    """将 LLM 调用过程写入日志，便于实验排查与复现。不记录 API Key；消息正文由 log_prompts 控制。"""

    def __init__(self, log_prompts: bool = False):
        super().__init__()
        self.log_prompts = log_prompts

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> None:
        run_id = kwargs.get("run_id", "")
        logger.info(
            "LLM 调用开始 run_id=%s prompts_count=%d",
            str(run_id)[:8] if run_id else "-",
            len(prompts),
        )
        if self.log_prompts and prompts:
            for i, p in enumerate(prompts):
                preview = (p[:200] + "…") if len(p) > 200 else p
                logger.info("LLM 请求[%d] preview: %s", i, preview)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        run_id = kwargs.get("run_id", "")
        gen = response.generations
        if gen and gen[0]:
            g = gen[0][0]
            usage = getattr(g, "message_usage", None) or getattr(
                g, "generation_info", {}
            )
            if isinstance(usage, dict):
                token_info = usage
            else:
                token_info = (
                    {
                        "input_tokens": getattr(usage, "input_tokens", None),
                        "output_tokens": getattr(usage, "output_tokens", None),
                    }
                    if usage
                    else {}
                )
        else:
            token_info = {}
        logger.info(
            "LLM 调用结束 run_id=%s generations=%d usage=%s",
            str(run_id)[:8] if run_id else "-",
            len(gen) if gen else 0,
            token_info,
        )

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        run_id = kwargs.get("run_id", "")
        logger.exception(
            "LLM 调用异常 run_id=%s error=%s",
            str(run_id)[:8] if run_id else "-",
            type(error).__name__,
        )


def _default_callbacks(log_prompts: bool = False) -> list[BaseCallbackHandler]:
    return [LLMCallbacksLogger(log_prompts=log_prompts)]


def get_aliyun_llm_env(
    model_key: str = "OPENAI_MODEL_NAME",
    model_default: str = "qwen-plus",
) -> Optional[dict[str, Any]]:
    """
    从环境变量读取阿里云百炼配置，供 CrewAI 等非 LangChain 调用方使用。
    调用前需已 load_dotenv；返回 dict 可直接用于 crewai.LLM(**result)。
    """
    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("ALIYUN_API_KEY")
    if not api_key:
        return None
    return {
        "model": os.getenv(model_key, model_default),
        "temperature": 0.7,
        "base_url": os.getenv(
            "DASHSCOPE_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        "api_key": api_key,
    }


def get_aliyun_llm(
    model: str = "qwen-plus",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    log_prompts: bool = False,
    **kwargs
):
    """
    获取阿里云百炼 LLM 实例

    Args:
        model: 模型名称，如 qwen-turbo, qwen-plus, qwen-max 等
        temperature: 温度参数
        max_tokens: 最大 token 数
        log_prompts: 为 True 时在日志中打印请求内容预览（前 200 字），便于调试
        **kwargs: 其他传递给 ChatOpenAI 的参数

    Returns:
        ChatOpenAI 实例
    """
    # 加载环境变量
    load_dotenv()

    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("ALIYUN_API_KEY")
    if not api_key:
        raise ValueError(
            "请设置 DASHSCOPE_API_KEY 或 ALIYUN_API_KEY 环境变量"
        )

    base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

    callbacks = list(_default_callbacks(log_prompts=log_prompts))
    if "callbacks" in kwargs:
        callbacks = callbacks + list(kwargs.pop("callbacks", []))
    kwargs["callbacks"] = callbacks
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    # ChatOpenAI 运行时接受 max_tokens，但类型桩未声明，用 cast 避免误报
    return ChatOpenAI(**cast(Any, {
        "model": model,
        "temperature": temperature,
        "api_key": SecretStr(api_key),
        "base_url": base_url,
        **kwargs,
    }))


def get_openai_llm(
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    log_prompts: bool = False,
    **kwargs
):
    """
    获取 OpenAI LLM 实例（备用）。同样会写入调用过程日志。
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY 环境变量")

    base_url = os.getenv("OPENAI_BASE_URL")  # 可选的代理 URL

    callbacks = list(_default_callbacks(log_prompts=log_prompts))
    if "callbacks" in kwargs:
        callbacks = callbacks + list(kwargs.pop("callbacks", []))
    kwargs["callbacks"] = callbacks

    llm_kwargs: dict[str, Any] = {
        "model": model,
        "temperature": temperature,
        "api_key": SecretStr(api_key),
        **kwargs
    }
    if base_url:
        llm_kwargs["base_url"] = base_url
    if max_tokens:
        llm_kwargs["max_tokens"] = max_tokens

    return ChatOpenAI(**cast(Any, llm_kwargs))
