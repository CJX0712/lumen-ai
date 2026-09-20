"""可注入的 Mock LLM —— 用于单元测试与全链路验证，无需 GPU / 网络。"""

from __future__ import annotations

from .base import BaseLLM, Message


class MockLLM(BaseLLM):
    def __init__(
        self,
        reply: str | None = None,
        replies: list[str] | None = None,
        echo: bool = False,
    ):
        self._fixed = reply
        self._queue = list(replies) if replies else None
        self.echo = echo

    def _next(self, prompt: str = "") -> str:
        if self._fixed is not None:
            return self._fixed
        if self._queue is not None:
            return self._queue.pop(0) if self._queue else "Final Answer: 结束"
        if self.echo:
            return f"[mock]{prompt}"
        return "This is a mock response."

    def complete(self, prompt: str, *, system: str | None = None, **kwargs) -> str:
        return self._next(prompt)

    def chat(self, messages: list[Message], **kwargs) -> str:
        last = messages[-1].content if messages else ""
        return self._next(last)
