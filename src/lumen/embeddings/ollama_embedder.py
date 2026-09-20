"""Ollama 嵌入后端（默认使用 nomic-embed-text）。"""

from __future__ import annotations

from .base import BaseEmbedder


class OllamaEmbedder(BaseEmbedder):
    def __init__(self, host: str, model: str, dim: int = 768, timeout: int = 120):
        try:
            import ollama
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("需要 ollama 包: pip install ollama") from e
        self._client = ollama.Client(host=host, timeout=timeout)
        self.model = model
        self._dim = dim

    @property
    def dim(self) -> int:
        return self._dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self._client.embed(model=self.model, input=texts)
        return resp["embeddings"]
