# 公共大模型封装，各阶段课程从此包引用。
# CrewAI 专用：阿里云通义千问
from .crew_aliyun_llm import AliyunLLM as CrewAliyunLLM
# LangChain 专用：阿里云通义千问
from .langchain_aliyun_llm import (
    LangChainAliyunLLM,
    create_aliyun_llm as create_langchain_aliyun_llm,
)
# LangGraph 专用：阿里云通义千问
from .langgraph_aliyun_llm import (
    LangGraphAliyunLLM,
    create_agent_node,
    create_aliyun_langgraph_llm,
    should_continue,
)
# LlamaIndex 专用：阿里云通义千问
from .llamaindex_aliyun_llm import (
    LlamaIndexAliyunLLM,
    create_aliyun_llm as create_llamaindex_aliyun_llm,
)

__all__ = [
    "CrewAliyunLLM",
    # LangChain
    "LangChainAliyunLLM",
    "create_langchain_aliyun_llm",
    # LangGraph
    "LangGraphAliyunLLM",
    "create_aliyun_langgraph_llm",
    "create_agent_node",
    "should_continue",
    # LlamaIndex
    "LlamaIndexAliyunLLM",
    "create_llamaindex_aliyun_llm",
]
