"""LLM 网关抽象接口。

屏蔽 Ollama / OpenAI 兼容 / Mock 等后端差异，调用方只依赖 BaseLLM。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    role: str  # system | user | assistant
    content: str

    @classmethod
    def system(cls, content: str) -> "Message":
        return cls("system", content)

    @classmethod
    def user(cls, content: str) -> "Message":
        return cls("user", content)

    @classmethod
    def assistant(cls, content: str) -> "Message":
        return cls("assistant", content)


class LLMError(Exception):
    """LLM 调用失败（网络、鉴权、模型缺失等）。"""


class BaseLLM(ABC):
    @abstractmethod
    def complete(self, prompt: str, *, system: str | None = None, **kwargs) -> str:
        """单次补全。"""

    @abstractmethod
    def chat(self, messages: list[Message], **kwargs) -> str:
        """多轮对话。"""
