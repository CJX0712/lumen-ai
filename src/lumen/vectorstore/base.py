"""向量库抽象接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    id: str
    score: float  # L2 距离，越小越相似
    text: str
    metadata: dict


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert(self, items: list[dict]) -> None:
        """items: [{'id': str, 'vector': list[float], 'text': str, 'metadata': dict}]"""

    @abstractmethod
    def search(self, query_vector: list[float], top_k: int = 4) -> list[SearchResult]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def save(self, path: str) -> None:
        ...

    @abstractmethod
    def load(self, path: str) -> None:
        ...
