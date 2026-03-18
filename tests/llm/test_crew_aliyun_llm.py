"""
AliyunLLM（llm.crew_aliyun_llm）单元测试。
使用 pytest，mock requests 与 os.getenv，不发起真实请求。
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests as requests_lib

from llm.crew_aliyun_llm import AliyunLLM


def _make_response(
    status_code: int = 200, json_data: dict | None = None, use_default_json: bool = True
) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    if json_data is not None or not use_default_json:
        resp.json.return_value = json_data if json_data is not None else {}
    else:
        resp.json.return_value = {"choices": [{"message": {"content": "ok"}}]}
    resp.raise_for_status = MagicMock()
    resp.text = ""
    resp.url = "https://example.com"
    return resp


# ---------- __init__ ----------


class TestInit:
    def test_init_with_api_key(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.model == "qwen-plus"
        assert llm.api_key == "sk-x"
        assert llm.region == "cn"
        assert "dashscope.aliyuncs.com" in llm.endpoint
        assert llm.image_model == "qwen3-vl-plus"
        assert llm.retry_count == 2
        assert llm.timeout == 600

    def test_init_api_key_from_env_aliyun(self):
        with patch("llm.crew_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-env" if k == "ALIYUN_API_KEY" else (d if d is not None else None)):
            llm = AliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-env"

    def test_init_api_key_from_env_dashscope(self):
        with patch("llm.crew_aliyun_llm.os.getenv", side_effect=lambda k, d=None: "sk-dash" if k == "DASHSCOPE_API_KEY" else None):
            llm = AliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-dash"

    def test_init_missing_api_key_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="API Key 未提供"):
                AliyunLLM(model="qwen-plus", api_key=None)

    def test_init_region_intl(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x", region="intl")
        assert "dashscope-intl" in llm.endpoint

    def test_init_region_finance(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x", region="finance")
        assert "dashscope-finance" in llm.endpoint

    def test_init_invalid_region_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="不支持的地域"):
                AliyunLLM(model="qwen-plus", api_key="sk-x", region="invalid")

    def test_init_custom_timeout_retry_image_model(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(
                model="qwen-turbo",
                api_key="sk-x",
                timeout=120,
                retry_count=3,
                image_model="qwen-vl-max",
            )
        assert llm.timeout == 120
        assert llm.retry_count == 3
        assert llm.image_model == "qwen-vl-max"


# ---------- _normalize_multimodal_tool_result ----------


class TestNormalizeMultimodal:
    def test_passthrough_non_assistant(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        msgs = [{"role": "user", "content": "hi"}]
        out, flag = llm._normalize_multimodal_tool_result(msgs)
        assert out == msgs
        assert flag is False

    def test_passthrough_assistant_non_string_content(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        msgs = [{"role": "assistant", "content": ["text", "image"]}]
        out, flag = llm._normalize_multimodal_tool_result(msgs)
        assert out == msgs
        assert flag is False

    def test_normalize_base64_data_url(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        content = "Add image to content Local xxx data:image/png;base64,abc123"
        msgs = [{"role": "assistant", "content": content}]
        out, flag = llm._normalize_multimodal_tool_result(msgs)
        assert len(out) == 1
        assert out[0]["role"] == "user"
        assert out[0]["content"][0]["type"] == "text"
        assert out[0]["content"][1]["type"] == "image_url"
        assert "data:image/png;base64,abc123" in out[0]["content"][1]["image_url"]["url"]
        assert flag is True

    def test_normalize_observation_http(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        content = "Add image to content Local Observation: http://example.com/img.jpg"
        msgs = [{"role": "assistant", "content": content}]
        out, flag = llm._normalize_multimodal_tool_result(msgs)
        assert len(out) == 1
        assert out[0]["role"] == "user"
        assert out[0]["content"][1]["type"] == "image"
        assert out[0]["content"][1]["image"] == "http://example.com/img.jpg"
        assert flag is True


# ---------- _validate_messages ----------


class TestValidateMessages:
    def test_valid_messages(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        llm._validate_messages([{"role": "user", "content": "hi"}])
        llm._validate_messages([{"role": "assistant", "content": "ok"}])
        llm._validate_messages([{"role": "tool", "tool_call_id": "id1", "content": "result"}])

    def test_invalid_role_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        with pytest.raises(ValueError, match="role"):
            llm._validate_messages([{"role": "invalid", "content": "x"}])

    def test_tool_missing_tool_call_id_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        with pytest.raises(ValueError, match="tool_call_id"):
            llm._validate_messages([{"role": "tool", "content": "x"}])


# ---------- _prepare_stop_words / get_context_window_size / supports_* ----------


class TestHelpers:
    def test_prepare_stop_words_str(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm._prepare_stop_words("END") == "END"
        assert llm._prepare_stop_words("") is None
        assert llm._prepare_stop_words(["a", "b"]) == ["a", "b"]

    def test_get_context_window_size(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm_long = AliyunLLM(model="qwen-long", api_key="sk-x")
            llm_plus = AliyunLLM(model="qwen-plus", api_key="sk-x")
            llm_other = AliyunLLM(model="qwen-other", api_key="sk-x")
        assert llm_long.get_context_window_size() == 200_000
        assert llm_plus.get_context_window_size() == 8192
        assert llm_other.get_context_window_size() == 8192

    def test_supports_function_calling_and_stop_words(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        assert llm.supports_function_calling() is True
        assert llm.supports_stop_words() is True


# ---------- call (mocked requests) ----------


class TestCall:
    def test_call_str_message_returns_content(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        with patch("llm.crew_aliyun_llm.requests.post", return_value=_make_response(200, {"choices": [{"message": {"content": "hello"}}]})):
            out = llm.call("hi")
        assert out == "hello"

    def test_call_list_messages_returns_content(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        with patch("llm.crew_aliyun_llm.requests.post", return_value=_make_response(200, {"choices": [{"message": {"content": "yes"}}]})):
            out = llm.call([{"role": "user", "content": "1+1=2?"}])
        assert out == "yes"

    def test_call_returns_tool_calls_when_no_available_functions(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        tool_calls = [{"id": "tc1", "function": {"name": "foo", "arguments": "{}"}}]
        with patch("llm.crew_aliyun_llm.requests.post", return_value=_make_response(200, {"choices": [{"message": {"content": None, "tool_calls": tool_calls}}]})):
            out = llm.call([{"role": "user", "content": "x"}], available_functions=None)
        assert out == tool_calls

    def test_call_max_iterations_zero_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        with pytest.raises(RuntimeError, match="最大迭代次数"):
            llm.call("x", available_functions={}, max_iterations=0)

    def test_call_missing_choices_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        resp = _make_response(200, json_data={"error": "no choices"}, use_default_json=False)
        with patch("llm.crew_aliyun_llm.requests.post", return_value=resp):
            with pytest.raises(ValueError, match="choices"):
                llm.call("x")

    def test_call_5xx_retry_then_raise(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x", retry_count=1)
        fail = _make_response(503, None)
        fail.text = "Service Unavailable"
        ok = _make_response(200, {"choices": [{"message": {"content": "ok"}}]})
        with patch("llm.crew_aliyun_llm.requests.post", side_effect=[fail, ok]):
            out = llm.call("hi")
        assert out == "ok"

    def test_call_5xx_exhaust_retries_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x", retry_count=1)
        fail = _make_response(503, json_data={}, use_default_json=False)
        fail.text = "Service Unavailable"
        fail.raise_for_status.side_effect = requests_lib.HTTPError("503")
        with patch("llm.crew_aliyun_llm.requests.post", return_value=fail):
            with pytest.raises(RuntimeError, match="请求失败"):
                llm.call("hi")

    def test_call_empty_content_retry_then_ok(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        empty = _make_response(200, {"choices": [{"message": {"content": ""}}]})
        ok = _make_response(200, {"choices": [{"message": {"content": "done"}}]})
        with patch("llm.crew_aliyun_llm.requests.post", side_effect=[empty, ok]):
            out = llm.call("hi", _retry_on_empty=True)
        assert out == "done"

    def test_call_empty_content_exhaust_raises(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        empty = _make_response(200, {"choices": [{"message": {"content": ""}}]})
        with patch("llm.crew_aliyun_llm.requests.post", return_value=empty):
            with pytest.raises(ValueError, match="空内容"):
                llm.call("hi", _retry_on_empty=True)


# ---------- _handle_function_calls (via call with available_functions) ----------


class TestHandleFunctionCalls:
    def test_call_with_available_functions_executes_and_recurs(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        tool_calls = [{"id": "tc1", "function": {"name": "add", "arguments": '{"a":1,"b":2}'}}]

        def add(a: int, b: int) -> int:
            return a + b

        # 第一次返回 tool_calls，第二次返回文本
        r1 = _make_response(200, {"choices": [{"message": {"content": None, "tool_calls": tool_calls}}]})
        r2 = _make_response(200, {"choices": [{"message": {"content": "done"}}]})
        with patch("llm.crew_aliyun_llm.requests.post", side_effect=[r1, r2]):
            out = llm.call(
                [{"role": "user", "content": "compute"}],
                available_functions={"add": add},
                max_iterations=5,
            )
        assert out == "done"


# ---------- acall ----------


class TestAcall:
    @pytest.mark.asyncio
    async def test_acall_returns_same_as_call(self):
        with patch("llm.crew_aliyun_llm.os.getenv", return_value=None):
            llm = AliyunLLM(model="qwen-plus", api_key="sk-x")
        with patch("llm.crew_aliyun_llm.requests.post", return_value=_make_response(200, {"choices": [{"message": {"content": "async_ok"}}]})):
            out = await llm.acall("hi")
        assert out == "async_ok"
