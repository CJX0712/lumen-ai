"""基于 faiss-cpu (IndexFlatL2) 的向量库实现，支持磁盘持久化。"""

from __future__ import annotations

import os
import pickle

from .base import BaseVectorStore, SearchResult


class FAISSVectorStore(BaseVectorStore):
    def __init__(self, dim: int):
        try:
            import faiss
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("需要 faiss-cpu: pip install faiss-cpu") from e
        self._faiss = faiss
        self.dim = dim
        self._index = faiss.IndexFlatL2(dim)
        self._texts: list[str] = []
        self._metas: list[dict] = []

    def upsert(self, items: list[dict]) -> None:
        if not items:
            return
        import numpy as np

        vecs = np.array([it["vector"] for it in items], dtype="float32")
        for it in items:
            self._texts.append(it.get("text", ""))
            self._metas.append(it.get("metadata", {}))
        self._index.add(vecs)

    def search(self, query_vector: list[float], top_k: int = 4) -> list[SearchResult]:
        import numpy as np

        if self.count() == 0:
            return []
        k = min(top_k, self.count())
        q = np.array([query_vector], dtype="float32")
        scores, idxs = self._index.search(q, k)
        out: list[SearchResult] = []
        for score, idx in zip(scores[0], idxs[0]):
            if int(idx) == -1:
                continue
            idx = int(idx)
            out.append(
                SearchResult(
                    id=str(idx),
                    score=float(score),
                    text=self._texts[idx],
                    metadata=self._metas[idx],
                )
            )
        return out

    def count(self) -> int:
        return int(self._index.ntotal)

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(
                {"texts": self._texts, "metas": self._metas, "dim": self.dim}, f
            )
        self._faiss.write_index(self._index, path + ".faiss")

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            data = pickle.load(f)
        self._texts = data["texts"]
        self._metas = data["metas"]
        self.dim = data["dim"]
        self._index = self._faiss.read_index(path + ".faiss")
