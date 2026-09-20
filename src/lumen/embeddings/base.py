"""文本向量化抽象接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """批量向量化，返回与输入等长的向量列表。"""

    @property
    @abstractmethod
    def dim(self) -> int:
        """向量维度。"""
