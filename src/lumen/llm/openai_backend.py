"""OpenAI 兼容后端（亦适用于任意兼容 /v1 接口的云端 / 自托管服务）。"""

from __future__ import annotations

from .base import BaseLLM, LLMError, Message


class OpenAIBackend(BaseLLM):
    def __init__(self, api_key: str, base_url: str, model: str, timeout: int = 120):
        if not api_key:
            raise LLMError("未配置 LUMEN_OPENAI_API_KEY")
        try:
            from openai import OpenAI
        except ImportError as e:  # pragma: no cover
            raise LLMError("需要 openai 包: pip install openai") from e
        self._client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        self.model = model

    def complete(self, prompt: str, *, system: str | None = None, **kwargs) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self._chat_dict(messages, kwargs)

    def chat(self, messages: list[Message], **kwargs) -> str:
        return self._chat_dict(
            [{"role": m.role, "content": m.content} for m in messages], kwargs
        )

    def _chat_dict(self, messages: list[dict], kwargs: dict) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.2),
            )
            return resp.choices[0].message.content or ""
        except Exception as e:  # noqa: BLE001
            raise LLMError(f"OpenAI 调用失败: {e}") from e
