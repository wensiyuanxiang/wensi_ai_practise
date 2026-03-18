"""
LangChainAliyunLLM 单元测试。
使用 pytest，mock ChatOpenAI 与 os.getenv，不发起真实请求。
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from llm.langchain_aliyun_llm import LangChainAliyunLLM, create_langchain_aliyun_llm


class TestInit:
    def test_init_with_api_key(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.model == "qwen-plus"
        assert llm.api_key == "sk-x"
        assert llm.region == "cn"
        assert "dashscope.aliyuncs.com" in llm.base_url
        mock_chat.assert_called_once()

    def test_init_api_key_from_env_aliyun(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI"):
            with patch("llm.langchain_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-env" if k == "ALIYUN_API_KEY" else (d if d is not None else None)):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-env"

    def test_init_api_key_from_env_dashscope(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI"):
            with patch("llm.langchain_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-dash" if k == "DASHSCOPE_API_KEY" else None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-dash"

    def test_init_missing_api_key_raises(self):
        with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="API Key 未提供"):
                LangChainAliyunLLM(model="qwen-plus", api_key=None)

    def test_init_region_intl(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI"):
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x", region="intl")
        assert "dashscope-intl" in llm.base_url

    def test_init_region_finance(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI"):
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x", region="finance")
        assert "dashscope-finance" in llm.base_url

    def test_init_invalid_region_raises(self):
        with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="不支持的地域"):
                LangChainAliyunLLM(model="qwen-plus", api_key="sk-x", region="invalid")

    def test_init_custom_params(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI"):
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(
                    model="qwen-turbo",
                    api_key="sk-x",
                    temperature=0.5,
                    timeout=120,
                    max_tokens=1024,
                )
        assert llm.temperature == 0.5
        assert llm.timeout == 120
        assert llm.max_tokens == 1024


class TestMethods:
    def test_as_langchain(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.as_langchain() is mock_instance

    def test_bind_tools(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        tools = [{"name": "test"}]
        result = llm.bind_tools(tools)
        mock_instance.bind_tools.assert_called_once_with(tools)
        assert result is llm

    def test_invoke(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.invoke.return_value = "response"
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = llm.invoke("hello")
        mock_instance.invoke.assert_called_once_with("hello")
        assert result == "response"

    @pytest.mark.asyncio
    async def test_ainvoke(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.ainvoke.return_value = "async_response"
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = await llm.ainvoke("hello")
        mock_instance.ainvoke.assert_called_once_with("hello")
        assert result == "async_response"

    def test_stream(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.stream.return_value = ["chunk1", "chunk2"]
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = list(llm.stream("hello"))
        mock_instance.stream.assert_called_once_with("hello")
        assert result == ["chunk1", "chunk2"]

    @pytest.mark.asyncio
    async def test_astream(self):
        async def mock_astream():
            yield "chunk1"
            yield "chunk2"

        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.astream.return_value = mock_astream()
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = [chunk async for chunk in llm.astream("hello")]
        mock_instance.astream.assert_called_once_with("hello")
        assert result == ["chunk1", "chunk2"]

    def test_getattr_proxy(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.some_attr = "value"
            mock_chat.return_value = mock_instance
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = LangChainAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.some_attr == "value"


class TestCreateFunction:
    def test_create_langchain_aliyun_llm(self):
        with patch("llm.langchain_aliyun_llm.ChatOpenAI"):
            with patch("llm.langchain_aliyun_llm.os.getenv", return_value=None):
                llm = create_langchain_aliyun_llm(model="qwen-turbo", api_key="sk-y")
        assert isinstance(llm, LangChainAliyunLLM)
        assert llm.model == "qwen-turbo"
        assert llm.api_key == "sk-y"
