"""LLM 模块入口：抽象接口、各后端实现与工厂函数。"""

from __future__ import annotations

from .base import BaseLLM, LLMError, Message
from .mock import MockLLM
from .ollama_backend import OllamaBackend
from .openai_backend import OpenAIBackend


def build_llm(settings) -> BaseLLM:
    """按配置构建 LLM 后端。"""
    backend = getattr(settings, "llm_backend", "ollama")
    if backend == "openai":
        return OpenAIBackend(
            settings.openai_api_key, settings.openai_base_url, settings.openai_model
        )
    if backend == "mock":
        return MockLLM()
    return OllamaBackend(settings.ollama_host, settings.ollama_model)


__all__ = [
    "BaseLLM",
    "LLMError",
    "Message",
    "MockLLM",
    "OllamaBackend",
    "OpenAIBackend",
    "build_llm",
]
