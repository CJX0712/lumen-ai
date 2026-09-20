"""工具抽象接口与结果类型。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolResult:
    output: str
    ok: bool = True


class BaseTool(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def run(self, inp: str) -> str:
        """执行工具，返回字符串结果（供 LLM 观测）。"""
