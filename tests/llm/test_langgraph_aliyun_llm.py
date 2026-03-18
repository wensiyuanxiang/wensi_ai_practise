"""
LangGraphAliyunLLM 单元测试。
使用 pytest，mock ChatOpenAI 与 os.getenv，不发起真实请求。
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from llm.langgraph_aliyun_llm import (
    LangGraphAliyunLLM,
    create_agent_node,
    create_aliyun_langgraph_llm,
    should_continue,
)


class TestInit:
    def test_init_with_api_key(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI") as mock_chat:
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.model == "qwen-plus"
        assert llm.api_key == "sk-x"
        assert llm.region == "cn"
        mock_chat.assert_called_once()

    def test_init_with_tools(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.bind_tools.return_value = mock_instance
            mock_chat.return_value = mock_instance
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                tools = [{"name": "test_tool"}]
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key="sk-x", tools=tools)
        mock_instance.bind_tools.assert_called_once_with(tools)

    def test_init_api_key_from_env(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI"):
            with patch("llm.langgraph_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-env" if k == "ALIYUN_API_KEY" else (d if d is not None else None)):
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-env"

    def test_init_missing_api_key_raises(self):
        with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="API Key 未提供"):
                LangGraphAliyunLLM(model="qwen-plus", api_key=None)


class TestMethods:
    def test_as_runnable(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.as_runnable() is mock_instance

    def test_create_agent_node_method(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.invoke.return_value = AIMessage(content="response")
            mock_chat.return_value = mock_instance
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key="sk-x")

        node = llm.create_agent_node(system_prompt="You are helpful")
        state = {"messages": [HumanMessage(content="hello")]}
        result = node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0].content == "response"

    def test_create_agent_node_with_system_prompt(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_instance.invoke.return_value = AIMessage(content="response")
            mock_chat.return_value = mock_instance
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key="sk-x")

        node = llm.create_agent_node(system_prompt="System prompt")
        state = {"messages": [HumanMessage(content="hello")]}
        node(state)

        # 检查是否正确地添加了 system prompt
        call_args = mock_instance.invoke.call_args[0][0]
        assert len(call_args) == 2
        assert isinstance(call_args[0], SystemMessage)
        assert call_args[0].content == "System prompt"

    def test_should_continue_method(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI"):
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                llm = LangGraphAliyunLLM(model="qwen-plus", api_key="sk-x")

        # 有 tool_calls 应该继续
        state_with_tools = {"messages": [AIMessage(content="", tool_calls=[{"name": "tool", "args": {}}])]}
        assert llm.should_continue(state_with_tools) == "tools"

        # 无 tool_calls 应该结束
        state_without_tools = {"messages": [AIMessage(content="done")]}
        assert llm.should_continue(state_without_tools) == "end"

        # 空消息列表应该结束
        empty_state = {"messages": []}
        assert llm.should_continue(empty_state) == "end"


class TestStandaloneFunctions:
    def test_create_agent_node_function(self):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="response")

        node = create_agent_node(mock_llm, system_prompt="You are helpful")
        state = {"messages": [HumanMessage(content="hello")]}
        result = node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0].content == "response"

    def test_should_continue_function(self):
        # 有 tool_calls 应该继续
        state_with_tools = {"messages": [AIMessage(content="", tool_calls=[{"name": "tool", "args": {}}])]}
        assert should_continue(state_with_tools) == "tools"

        # 无 tool_calls 应该结束
        state_without_tools = {"messages": [AIMessage(content="done")]}
        assert should_continue(state_without_tools) == "end"

        # 空消息列表应该结束
        empty_state = {"messages": []}
        assert should_continue(empty_state) == "end"


class TestCreateFunction:
    def test_create_aliyun_langgraph_llm(self):
        with patch("llm.langgraph_aliyun_llm.ChatOpenAI"):
            with patch("llm.langgraph_aliyun_llm.os.getenv", return_value=None):
                llm = create_aliyun_langgraph_llm(model="qwen-turbo", api_key="sk-y")
        assert isinstance(llm, LangGraphAliyunLLM)
        assert llm.model == "qwen-turbo"
        assert llm.api_key == "sk-y"
