"""向量库模块入口。"""

from __future__ import annotations

from .base import BaseVectorStore, SearchResult
from .faiss_store import FAISSVectorStore


def build_vectorstore(settings) -> BaseVectorStore:
    from ..embeddings import build_embedder

    emb = build_embedder(settings)
    return FAISSVectorStore(emb.dim)


__all__ = ["BaseVectorStore", "SearchResult", "FAISSVectorStore", "build_vectorstore"]
