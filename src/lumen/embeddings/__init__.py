"""嵌入模块入口。"""

from __future__ import annotations

from .base import BaseEmbedder
from .mock import MockEmbedder
from .ollama_embedder import OllamaEmbedder


def build_embedder(settings) -> BaseEmbedder:
    backend = getattr(settings, "embed_backend", "ollama")
    if backend == "mock":
        return MockEmbedder(getattr(settings, "embed_dim", 8))
    return OllamaEmbedder(
        settings.ollama_host, settings.ollama_embed_model, settings.embed_dim
    )


__all__ = ["BaseEmbedder", "MockEmbedder", "OllamaEmbedder", "build_embedder"]
