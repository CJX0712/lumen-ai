"""滑动窗口对话记忆。"""

from __future__ import annotations

from .base import BaseMemory, Turn


class ConversationMemory(BaseMemory):
    def __init__(self, window: int = 6):
        self.window = window
        self._turns: list[Turn] = []

    def add(self, user: str, assistant: str) -> None:
        self._turns.append(Turn(user, assistant))
        if self.window and len(self._turns) > self.window:
            self._turns = self._turns[-self.window:]

    def get_context(self) -> str:
        lines = []
        for t in self._turns:
            lines.append(f"用户: {t.user}")
            lines.append(f"助手: {t.assistant}")
        return "\n".join(lines)

    def clear(self) -> None:
        self._turns = []
