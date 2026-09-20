"""对话记忆抽象接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Turn:
    user: str
    assistant: str


class BaseMemory(ABC):
    @abstractmethod
    def add(self, user: str, assistant: str) -> None:
        ...

    @abstractmethod
    def get_context(self) -> str:
        """返回供 LLM 参考的历史上下文文本。"""

    @abstractmethod
    def clear(self) -> None:
        ...
