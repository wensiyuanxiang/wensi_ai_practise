"""
LlamaIndexAliyunLLM 单元测试。
使用 pytest，mock OpenAILike 与 os.getenv，不发起真实请求。
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from llm.llamaindex_aliyun_llm import LlamaIndexAliyunLLM, create_llamaindex_aliyun_llm


class TestInit:
    def test_init_with_api_key(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.model == "qwen-plus"
        assert llm.api_key == "sk-x"
        assert llm.region == "cn"
        assert "dashscope.aliyuncs.com" in llm.api_base
        mock_openai.assert_called_once()

    def test_init_api_key_from_env_aliyun(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike"):
            with patch("llm.llamaindex_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-env" if k == "ALIYUN_API_KEY" else (d if d is not None else None)):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-env"

    def test_init_api_key_from_env_dashscope(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike"):
            with patch("llm.llamaindex_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-dash" if k == "DASHSCOPE_API_KEY" else None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-dash"

    def test_init_missing_api_key_raises(self):
        with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="API Key 未提供"):
                LlamaIndexAliyunLLM(model="qwen-plus", api_key=None)

    def test_init_region_intl(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike"):
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x", region="intl")
        assert "dashscope-intl" in llm.api_base

    def test_init_region_finance(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike"):
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x", region="finance")
        assert "dashscope-finance" in llm.api_base

    def test_init_invalid_region_raises(self):
        with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="不支持的地域"):
                LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x", region="invalid")

    def test_init_custom_params(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike"):
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(
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
    def test_as_llamaindex(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.as_llamaindex() is mock_instance

    def test_complete(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.complete.return_value = "response"
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = llm.complete("hello")
        mock_instance.complete.assert_called_once_with("hello")
        assert result == "response"

    @pytest.mark.asyncio
    async def test_acomplete(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.acomplete.return_value = "async_response"
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = await llm.acomplete("hello")
        mock_instance.acomplete.assert_called_once_with("hello")
        assert result == "async_response"

    def test_chat(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "chat_response"
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = llm.chat([{"role": "user", "content": "hi"}])
        mock_instance.chat.assert_called_once_with([{"role": "user", "content": "hi"}])
        assert result == "chat_response"

    @pytest.mark.asyncio
    async def test_achat(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.achat.return_value = "async_chat_response"
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = await llm.achat([{"role": "user", "content": "hi"}])
        mock_instance.achat.assert_called_once_with([{"role": "user", "content": "hi"}])
        assert result == "async_chat_response"

    def test_stream_complete(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.stream_complete.return_value = ["chunk1", "chunk2"]
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = list(llm.stream_complete("hello"))
        mock_instance.stream_complete.assert_called_once_with("hello")
        assert result == ["chunk1", "chunk2"]

    @pytest.mark.asyncio
    async def test_astream_complete(self):
        async def mock_astream():
            yield "chunk1"
            yield "chunk2"

        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.astream_complete.return_value = mock_astream()
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = [chunk async for chunk in llm.astream_complete("hello")]
        mock_instance.astream_complete.assert_called_once_with("hello")
        assert result == ["chunk1", "chunk2"]

    def test_stream_chat(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.stream_chat.return_value = ["chunk1", "chunk2"]
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = list(llm.stream_chat([{"role": "user", "content": "hi"}]))
        mock_instance.stream_chat.assert_called_once_with([{"role": "user", "content": "hi"}])
        assert result == ["chunk1", "chunk2"]

    @pytest.mark.asyncio
    async def test_astream_chat(self):
        async def mock_astream():
            yield "chunk1"
            yield "chunk2"

        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.astream_chat.return_value = mock_astream()
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        result = [chunk async for chunk in llm.astream_chat([{"role": "user", "content": "hi"}])]
        mock_instance.astream_chat.assert_called_once_with([{"role": "user", "content": "hi"}])
        assert result == ["chunk1", "chunk2"]

    def test_getattr_proxy(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike") as mock_openai:
            mock_instance = MagicMock()
            mock_instance.some_attr = "value"
            mock_openai.return_value = mock_instance
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = LlamaIndexAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.some_attr == "value"


class TestCreateFunction:
    def test_create_llamaindex_aliyun_llm(self):
        with patch("llm.llamaindex_aliyun_llm.OpenAILike"):
            with patch("llm.llamaindex_aliyun_llm.os.getenv", return_value=None):
                llm = create_llamaindex_aliyun_llm(model="qwen-turbo", api_key="sk-y")
        assert isinstance(llm, LlamaIndexAliyunLLM)
        assert llm.model == "qwen-turbo"
        assert llm.api_key == "sk-y"
