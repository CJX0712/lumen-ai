"""确定性 Mock 嵌入器 —— 单元测试用，不依赖模型，向量经 L2 归一化。"""

from __future__ import annotations

import hashlib
import math

from .base import BaseEmbedder


class MockEmbedder(BaseEmbedder):
    def __init__(self, dim: int = 8):
        self._dim = dim

    @property
    def dim(self) -> int:
        return self._dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        out = []
        for t in texts:
            vec = [0.0] * self._dim
            for i in range(self._dim):
                h = hashlib.md5(f"{t}::{i}".encode("utf-8")).digest()
                vec[i] = (int.from_bytes(h[:4], "big") / 2**32) * 2 - 1
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            out.append([v / norm for v in vec])
        return out
