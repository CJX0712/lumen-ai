"""视觉语言模型（图片描述 / OCR）抽象接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod


class VisionLLM(ABC):
    @abstractmethod
    def caption(self, image_path: str, prompt: str = "描述这张图片的内容") -> str:
        """返回图片的文本描述（可作为 RAG 的文本来源）。"""
