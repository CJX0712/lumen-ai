"""ReAct 智能体：思考 → 调用工具 → 观测 → 最终回答，可多轮循环。"""

from __future__ import annotations

import re

from ..llm.base import BaseLLM, Message
from ..memory.base import BaseMemory
from ..tools.registry import ToolRegistry


class Agent:
    def __init__(
        self,
        llm: BaseLLM,
        tools: ToolRegistry,
        memory: BaseMemory | None = None,
        max_steps: int = 6,
    ):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.max_steps = max_steps

    def _prompt(self, question: str, history: str, trail: str) -> str:
        tools_desc = self.tools.describe()
        parts = [
            "你是一个可以使用工具的智能体。按需思考并调用工具，最终给出答案。",
            "可用工具:\n" + tools_desc,
            "严格按以下格式输出(可多轮):",
            "Thought: <你的思考>",
            "Action: <工具名>[<输入>]",
            "Observation: <工具返回，由系统填充>",
            "...(可重复)...",
            "当能回答时输出:",
            "Final Answer: <最终回答>\n",
        ]
        if history:
            parts.append("历史对话:\n" + history)
        if trail:
            parts.append("目前为止的推理轨迹:\n" + trail)
        parts.append(f"问题: {question}\n")
        return "\n".join(parts)

    @staticmethod
    def _parse_action(text: str):
        m = re.search(r"Action:\s*([^\[\]]+)\s*\[([^\]]*)\]", text)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        return None, None

    def run(self, question: str) -> str:
        history = self.memory.get_context() if self.memory else ""
        trail = ""
        answer = ""
        for _ in range(self.max_steps):
            prompt = self._prompt(question, history, trail)
            resp = self.llm.complete(prompt)
            trail += resp + "\n"

            name, inp = self._parse_action(resp)
            if "Final Answer:" in resp:
                answer = resp.split("Final Answer:")[-1].strip()
                break

            if name:
                tool = self.tools.get(name)
                obs = tool.run(inp) if tool else f"未知工具: {name}"
                trail += f"Observation: {obs}\n"
                continue

            # 既没有 Action 也没有 Final Answer：引导收尾
            trail += "Observation: 请输出 Final Answer。\n"

        if not answer:
            answer = trail.strip()

        if self.memory:
            self.memory.add(question, answer)
        return answer
