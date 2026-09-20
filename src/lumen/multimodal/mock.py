"""Mock 视觉模型 —— 单元测试用，返回确定性描述。"""

from __future__ import annotations

from .base import VisionLLM


class MockVision(VisionLLM):
    def __init__(self, reply: str = "[图片内容描述：一只猫坐在窗边]"):
        self.reply = reply

    def caption(self, image_path: str, prompt: str = "描述这张图片的内容") -> str:
        return self.reply
