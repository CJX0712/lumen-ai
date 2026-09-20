"""多模态模块入口：视觉语言模型（图片描述）抽象与实现。"""

from __future__ import annotations

from .base import VisionLLM
from .mock import MockVision
from .ollama_vision import OllamaVision


def build_vision(settings) -> VisionLLM:
    backend = getattr(settings, "vision_backend", "ollama")
    if backend == "mock":
        return MockVision()
    return OllamaVision(settings.ollama_host, settings.ollama_vision_model)


__all__ = ["VisionLLM", "MockVision", "OllamaVision", "build_vision"]
