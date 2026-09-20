"""工具模块入口。"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .builtin import CalculatorTool, DateTimeTool, EchoTool
from .calculator import safe_calc
from .registry import ToolRegistry


def build_registry() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(CalculatorTool())
    reg.register(DateTimeTool())
    reg.register(EchoTool())
    return reg


__all__ = [
    "BaseTool",
    "ToolResult",
    "ToolRegistry",
    "CalculatorTool",
    "DateTimeTool",
    "EchoTool",
    "safe_calc",
    "build_registry",
]
