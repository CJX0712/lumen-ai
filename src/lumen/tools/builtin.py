"""内置工具：计算器 / 时间 / 回声调试。"""

from __future__ import annotations

from datetime import datetime, timezone

from .base import BaseTool
from .calculator import safe_calc


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "计算算术表达式，例如 'calculator[ (12+8)*3 ]'。支持 + - * / ** % 与括号。"

    def run(self, inp: str) -> str:
        try:
            return str(safe_calc(inp.strip()))
        except Exception as e:  # noqa: BLE001
            return f"计算错误: {e}"


class DateTimeTool(BaseTool):
    name = "datetime"
    description = "返回当前 UTC 时间，例如 'datetime[]'。"

    def run(self, inp: str) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


class EchoTool(BaseTool):
    name = "echo"
    description = "原样返回输入，便于调试，例如 'echo[hello]'。"

    def run(self, inp: str) -> str:
        return inp
