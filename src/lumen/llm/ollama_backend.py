"""Ollama 本地后端（CPU 友好，默认路径）。"""

from __future__ import annotations

from .base import BaseLLM, LLMError, Message


class OllamaBackend(BaseLLM):
    def __init__(self, host: str, model: str, timeout: int = 120):
        self.host = host
        self.model = model
        self.timeout = timeout
        try:
            import ollama
        except ImportError as e:  # pragma: no cover
            raise LLMError("需要 ollama 包: pip install ollama") from e
        self._client = ollama.Client(host=host, timeout=timeout)

    def complete(self, prompt: str, *, system: str | None = None, **kwargs) -> str:
        try:
            resp = self._client.generate(
                model=self.model,
                prompt=prompt,
                system=system or "",
                options={"temperature": kwargs.get("temperature", 0.2)},
            )
            return resp["response"]
        except Exception as e:  # noqa: BLE001
            raise LLMError(f"Ollama 调用失败: {e}") from e

    def chat(self, messages: list[Message], **kwargs) -> str:
        try:
            resp = self._client.chat(
                model=self.model,
                messages=[{"role": m.role, "content": m.content} for m in messages],
                options={"temperature": kwargs.get("temperature", 0.2)},
            )
            return resp["message"]["content"]
        except Exception as e:  # noqa: BLE001
            raise LLMError(f"Ollama 调用失败: {e}") from e
